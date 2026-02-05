import pytest
import allure
from utils.driver_setup import DriverSetup
from pages.login_page import LoginPage
from config import Config

@allure.feature("登录功能测试")
class TestLogin:
    @pytest.fixture(autouse=True)
    def setup(self):
        """测试前置条件"""
        self.driver = DriverSetup.get_driver()
        self.login_page = LoginPage(self.driver)
        yield
        self.driver.quit()
    
    @allure.story("测试有效登录")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_valid_login(self):
        """测试有效用户登录"""
        with allure.step("1. 打开登录页面"):
            self.login_page.open()
            
        with allure.step("2. 输入有效用户名密码"):
            self.login_page.login(Config.VALID_USERNAME, Config.VALID_PASSWORD)
            
        with allure.step("3. 验证登录成功"):
            assert self.login_page.is_login_successful(), "登录失败"
            
        with allure.step("4. 截图验证"):
            self.driver.save_screenshot(f"{Config.SCREENSHOT_DIR}test_valid_login.png")
    
    @allure.story("测试无效登录")
    def test_invalid_login(self):
        """测试无效用户登录"""
        with allure.step("1. 打开登录页面"):
            self.login_page.open()
            
        with allure.step("2. 输入无效用户名密码"):
            self.login_page.login(Config.INVALID_USERNAME, Config.INVALID_PASSWORD)
            
        with allure.step("3. 验证显示错误信息"):
            error_message = self.login_page.get_error_message()
            assert error_message is not None, "应该显示错误信息"
            assert "Username and password do not match" in error_message
            
        with allure.step("4. 截图验证"):
            self.driver.save_screenshot(f"{Config.SCREENSHOT_DIR}test_invalid_login.png")
    
    @allure.story("测试空密码登录")
    def test_login_with_empty_password(self):
        """测试空密码登录"""
        with allure.step("1. 打开登录页面"):
            self.login_page.open()
            
        with allure.step("2. 输入用户名，密码为空"):
            self.login_page.login(Config.VALID_USERNAME, "")
            
        with allure.step("3. 验证显示错误信息"):
            error_message = self.login_page.get_error_message()
            assert error_message is not None, "应该显示错误信息"
            assert "Password is required" in error_message