import pytest
import allure
from utils.driver_setup import DriverSetup
from pages.login_page import LoginPage
from pages.home_page import HomePage
from config import Config

@allure.feature("商品功能测试")
class TestProduct:
    @pytest.fixture(autouse=True)
    def setup(self):
        """测试前置条件：先登录"""
        self.driver = DriverSetup.get_driver()
        self.login_page = LoginPage(self.driver)
        self.home_page = HomePage(self.driver)
        
        # 先登录
        self.login_page.open().login(Config.VALID_USERNAME, Config.VALID_PASSWORD)
        yield
        self.driver.quit()
    
    @allure.story("测试添加商品到购物车")
    def test_add_to_cart(self):
        """测试添加商品到购物车"""
        with allure.step("1. 获取初始购物车数量"):
            initial_count = self.home_page.get_cart_count()
            
        with allure.step("2. 添加商品到购物车"):
            self.home_page.add_first_product_to_cart()
            
        with allure.step("3. 验证购物车数量增加"):
            new_count = self.home_page.get_cart_count()
            assert new_count == initial_count + 1, f"购物车数量应该从{initial_count}增加到{new_count}"
            
        with allure.step("4. 截图验证"):
            self.driver.save_screenshot(f"{Config.SCREENSHOT_DIR}test_add_to_cart.png")
    
    @allure.story("测试查看购物车")
    def test_view_cart(self):
        """测试查看购物车"""
        with allure.step("1. 添加商品到购物车"):
            self.home_page.add_first_product_to_cart()
            
        with allure.step("2. 进入购物车页面"):
            cart_page = self.home_page.go_to_cart()
            
        with allure.step("3. 验证购物车中有商品"):
            cart_items = cart_page.get_cart_items_count()
            assert cart_items > 0, "购物车中应该有商品"
            
        with allure.step("4. 截图验证"):
            self.driver.save_screenshot(f"{Config.SCREENSHOT_DIR}test_view_cart.png")