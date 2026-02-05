# 配置文件
class Config:
    # 测试网站（使用演示网站）
    BASE_URL = "https://www.saucedemo.com/"

    # 浏览器配置
    BROWSER = "edge"  # chrome, firefox, edge
    HEADLESS = False
    IMPLICIT_WAIT = 10
    EXPLICIT_WAIT = 20

    # 测试数据
    VALID_USERNAME = "standard_user"
    VALID_PASSWORD = "secret_sauce"
    INVALID_USERNAME = "invalid_user"
    INVALID_PASSWORD = "invalid_pass"

    # 报告配置（注意：你项目里很多地方用字符串拼接，所以保留末尾 /）
    SCREENSHOT_DIR = "reports/screenshots/"
    REPORT_DIR = "reports/"

    # ✅ 日志配置（新增）
    LOG_DIR = "reports/logs/"
    LOG_LEVEL = "INFO"  # DEBUG / INFO / WARNING / ERROR
