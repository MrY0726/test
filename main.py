import os
import time

from config import Config
from utils.driver_setup import DriverSetup
from utils.logger import get_logger

from pages.login_page import LoginPage
from pages.home_page import HomePage


def demo_full_workflow():
    """演示完整的用户工作流程"""
    logger = get_logger("demo")

    # 确保截图目录存在（你项目里直接拼字符串写文件名）
    os.makedirs(Config.SCREENSHOT_DIR, exist_ok=True)

    logger.info("=== 开始演示电商网站自动化测试 ===")

    driver = DriverSetup.get_driver()

    try:
        # 1. 登录
        logger.info("1. 登录网站...")
        login_page = LoginPage(driver)
        login_page.open().login(Config.VALID_USERNAME, Config.VALID_PASSWORD)

        if login_page.is_login_successful():
            logger.info("✓ 登录成功")
        else:
            logger.error("✗ 登录失败")
            driver.save_screenshot(f"{Config.SCREENSHOT_DIR}demo_login_failed.png")
            return

        time.sleep(1)

        # 2. 浏览首页
        logger.info("2. 浏览商品...")
        home_page = HomePage(driver)
        product_count = home_page.get_product_count()
        logger.info("✓ 找到 %s 个商品", product_count)

        # 3. 添加商品到购物车
        logger.info("3. 添加商品到购物车...")
        if home_page.add_first_product_to_cart():
            cart_count = home_page.get_cart_count()
            logger.info("✓ 已添加商品到购物车，购物车数量: %s", cart_count)
        else:
            logger.error("✗ 添加商品失败")
            driver.save_screenshot(f"{Config.SCREENSHOT_DIR}demo_add_to_cart_failed.png")

        time.sleep(1)

        # 4. 查看购物车
        logger.info("4. 查看购物车...")
        cart_page = home_page.go_to_cart()
        cart_items = cart_page.get_cart_items_count()
        logger.info("✓ 购物车中有 %s 个商品", cart_items)

        time.sleep(1)

        # 5. 返回首页
        logger.info("5. 返回首页...")
        driver.back()
        time.sleep(1)

        # 6. 登出
        logger.info("6. 登出...")
        home_page.logout()
        logger.info("✓ 登出成功")

        logger.info("=== 演示完成 ===")

    except Exception:
        logger.exception("✗ 执行过程中出错（已记录堆栈）")
        try:
            driver.save_screenshot(f"{Config.SCREENSHOT_DIR}demo_exception.png")
        except Exception:
            pass
    finally:
        driver.quit()
        logger.info("浏览器已关闭")


if __name__ == "__main__":
    demo_full_workflow()
