import os
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options as EdgeOptions

from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager

from config import Config


class DriverSetup:
    @staticmethod
    def _ensure_dirs():
        report_dir = Path(getattr(Config, "REPORT_DIR", "reports"))
        screenshot_dir = Path(getattr(Config, "SCREENSHOT_DIR", "reports/screenshots"))
        report_dir.mkdir(parents=True, exist_ok=True)
        screenshot_dir.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def get_driver():
        """初始化 WebDriver（Windows 友好：本地驱动 > Selenium Manager > webdriver-manager）"""
        DriverSetup._ensure_dirs()

        browser = (getattr(Config, "BROWSER", "edge") or "edge").lower().strip()
        headless = bool(getattr(Config, "HEADLESS", False))

        if browser == "chrome":
            options = ChromeOptions()
            if headless:
                options.add_argument("--headless=new")
            options.add_argument("--window-size=1920,1080")

            local = os.getenv("CHROME_DRIVER_PATH") or getattr(Config, "CHROME_DRIVER_PATH", "")
            if local and Path(local).exists():
                service = ChromeService(executable_path=local)
                driver = webdriver.Chrome(service=service, options=options)
            else:
                # Selenium Manager（优先）
                try:
                    driver = webdriver.Chrome(options=options)
                except Exception:
                    # webdriver-manager（兜底）
                    service = ChromeService(ChromeDriverManager().install())
                    driver = webdriver.Chrome(service=service, options=options)

        elif browser == "firefox":
            options = FirefoxOptions()
            if headless:
                options.add_argument("-headless")

            local = os.getenv("GECKO_DRIVER_PATH") or getattr(Config, "GECKO_DRIVER_PATH", "")
            if local and Path(local).exists():
                service = FirefoxService(executable_path=local)
                driver = webdriver.Firefox(service=service, options=options)
            else:
                try:
                    driver = webdriver.Firefox(options=options)
                except Exception:
                    service = FirefoxService(GeckoDriverManager().install())
                    driver = webdriver.Firefox(service=service, options=options)

        elif browser == "edge":
            options = EdgeOptions()
            if headless:
                options.add_argument("--headless=new")
            options.add_argument("--window-size=1920,1080")

            # 1) 本地驱动（最稳，推荐）
            local = os.getenv("EDGE_DRIVER_PATH") or getattr(Config, "EDGE_DRIVER_PATH", "")
            if local and Path(local).exists():
                service = EdgeService(executable_path=local)
                driver = webdriver.Edge(service=service, options=options)
            else:
                # 2) Selenium Manager（优先）
                try:
                    driver = webdriver.Edge(options=options)
                except Exception:
                    # 3) webdriver-manager（兜底：把下载源从 azureedge 换成 microsoft.com）
                    url = getattr(Config, "EDGE_WDM_URL", "https://msedgedriver.microsoft.com/")
                    latest = getattr(Config, "EDGE_WDM_LATEST_RELEASE_URL", "https://msedgedriver.microsoft.com/LATEST_RELEASE")
                    path = EdgeChromiumDriverManager(url=url, latest_release_url=latest).install()
                    service = EdgeService(executable_path=path)
                    driver = webdriver.Edge(service=service, options=options)
        else:
            raise ValueError(f"不支持的浏览器: {browser}")

        driver.implicitly_wait(getattr(Config, "IMPLICIT_WAIT", 10))
        try:
            driver.maximize_window()
        except Exception:
            pass
        return driver
