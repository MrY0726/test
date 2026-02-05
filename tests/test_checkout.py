import pytest
import allure
from utils.driver_setup import DriverSetup
from pages.login_page import LoginPage
from pages.home_page import HomePage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from config import Config

@allure.feature("结算功能测试")
class TestCheckout:
    @pytest.fixture(autouse=True)
    def setup(self):
        """测试前置条件：登录并添加商品到购物车"""
        self.driver = DriverSetup.get_driver()
        self.login_page = LoginPage(self.driver)
        self.home_page = HomePage(self.driver)
        self.cart_page = CartPage(self.driver)
        self.checkout_page = CheckoutPage(self.driver)
        
        # 登录并添加商品
        self.login_page.open().login(Config.VALID_USERNAME, Config.VALID_PASSWORD)
        self.home_page.add_first_product_to_cart()
        self.home_page.go_to_cart()
        
        yield
        
        # 清理：登出
        try:
            self.home_page.logout()
        except:
            pass
        finally:
            self.driver.quit()
    
    @allure.story("测试完整的结算流程")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_complete_checkout_flow(self):
        """测试完整的结算流程：登录→添加商品→结算→完成订单"""
        with allure.step("1. 验证购物车中有商品"):
            cart_items = self.cart_page.get_cart_items_count()
            assert cart_items > 0, "购物车应该包含商品"
            allure.attach(f"购物车商品数量: {cart_items}", name="Cart Info")
        
        with allure.step("2. 点击结算按钮"):
            self.cart_page.click_checkout()
            assert "checkout-step-one.html" in self.driver.current_url
            self.driver.save_screenshot(f"{Config.SCREENSHOT_DIR}checkout_step1.png")
        
        with allure.step("3. 填写收货信息"):
            self.checkout_page.enter_checkout_info("张", "三", "100000")
            allure.attach("收货信息: 张三, 100000", name="Shipping Info")
        
        with allure.step("4. 继续到第二步"):
            self.checkout_page.click_continue()
            assert "checkout-step-two.html" in self.driver.current_url
            self.driver.save_screenshot(f"{Config.SCREENSHOT_DIR}checkout_step2.png")
        
        with allure.step("5. 验证订单摘要"):
            summary = self.checkout_page.get_order_summary()
            assert "Payment Information" in summary
            assert "Shipping Information" in summary
            assert "Price Total" in summary
            allure.attach(summary, name="Order Summary")
        
        with allure.step("6. 完成订单"):
            self.checkout_page.click_finish()
            assert "checkout-complete.html" in self.driver.current_url
            self.driver.save_screenshot(f"{Config.SCREENSHOT_DIR}checkout_complete.png")
        
        with allure.step("7. 验证订单完成信息"):
            success_message = self.checkout_page.get_success_message()
            assert "Thank you for your order" in success_message
            assert self.checkout_page.is_order_complete()
            print(f"订单完成信息: {success_message}")
    
    @allure.story("测试结算信息验证")
    def test_checkout_information_validation(self):
        """测试结算信息的表单验证"""
        with allure.step("1. 进入结算页面"):
            self.cart_page.click_checkout()
        
        with allure.step("2. 测试空信息提交"):
            self.checkout_page.click_continue()  # 不填写信息直接提交
            
            error_message = self.checkout_page.get_error_message()
            assert error_message is not None
            assert "First Name is required" in error_message
            allure.attach(f"错误信息: {error_message}", name="Validation Error")
        
        with allure.step("3. 测试只填写姓氏"):
            self.checkout_page.enter_checkout_info("", "李", "")
            self.checkout_page.click_continue()
            
            error_message = self.checkout_page.get_error_message()
            assert "First Name is required" in error_message
        
        with allure.step("4. 测试只填写名字"):
            self.checkout_page.enter_checkout_info("王", "", "")
            self.checkout_page.click_continue()
            
            error_message = self.checkout_page.get_error_message()
            assert "Last Name is required" in error_message
        
        with allure.step("5. 测试只填写邮编"):
            self.checkout_page.enter_checkout_info("", "", "200000")
            self.checkout_page.click_continue()
            
            error_message = self.checkout_page.get_error_message()
            assert "First Name is required" in error_message
    
    @allure.story("测试取消结算流程")
    def test_cancel_checkout_flow(self):
        """测试取消结算流程的不同阶段"""
        with allure.step("1. 进入结算第一步"):
            self.cart_page.click_checkout()
        
        with allure.step("2. 在第一步取消"):
            self.checkout_page.click_cancel()
            assert "cart.html" in self.driver.current_url
            self.driver.save_screenshot(f"{Config.SCREENSHOT_DIR}cancel_step1.png")
        
        with allure.step("3. 重新进入结算并填写信息"):
            self.cart_page.click_checkout()
            self.checkout_page.enter_checkout_info("赵", "六", "300000")
            self.checkout_page.click_continue()
        
        with allure.step("4. 在第二步取消"):
            self.checkout_page.click_cancel()
            assert "inventory.html" in self.driver.current_url
            self.driver.save_screenshot(f"{Config.SCREENSHOT_DIR}cancel_step2.png")
    
    @allure.story("测试订单总价计算")
    def test_order_total_calculation(self):
        """测试订单总价的计算是否正确"""
        with allure.step("1. 进入结算第二步"):
            self.cart_page.click_checkout()
            self.checkout_page.enter_checkout_info("钱", "七", "400000")
            self.checkout_page.click_continue()
        
        with allure.step("2. 获取价格信息"):
            item_total = self.checkout_page.get_item_total()
            tax_amount = self.checkout_page.get_tax_amount()
            total_amount = self.checkout_page.get_total_amount()
            
            allure.attach(f"商品小计: {item_total}", name="Item Total")
            allure.attach(f"税费: {tax_amount}", name="Tax")
            allure.attach(f"总计: {total_amount}", name="Total")
        
        with allure.step("3. 验证价格计算"):
            # 验证总价 = 商品小计 + 税费
            calculated_total = item_total + tax_amount
            assert abs(calculated_total - total_amount) < 0.01, "价格计算不正确"
            print(f"价格验证: {item_total} + {tax_amount} = {calculated_total} (页面总计: {total_amount})")
    
    @allure.story("测试多商品结算")
    def test_multiple_items_checkout(self):
        """测试多个商品同时结算"""
        with allure.step("1. 添加多个商品到购物车"):
            # 返回首页添加更多商品
            self.driver.get(Config.BASE_URL + "inventory.html")
            
            # 添加第二个商品
            self.home_page.add_product_by_index(1)  # 添加第二个商品
            cart_count = self.home_page.get_cart_count()
            assert cart_count == 2, f"购物车应该有2个商品，实际有{cart_count}个"
            
            allure.attach(f"购物车商品数量: {cart_count}", name="Cart Count")
        
        with allure.step("2. 进入购物车验证"):
            self.home_page.go_to_cart()
            cart_items = self.cart_page.get_cart_items_count()
            assert cart_items == 2, f"购物车应该显示2个商品"
        
        with allure.step("3. 完成结算流程"):
            self.cart_page.click_checkout()
            self.checkout_page.enter_checkout_info("孙", "八", "500000")
            self.checkout_page.click_continue()
            self.checkout_page.click_finish()
            
            assert self.checkout_page.is_order_complete()
            self.driver.save_screenshot(f"{Config.SCREENSHOT_DIR}multiple_items_checkout.png")
    
    @pytest.mark.parametrize("first_name,last_name,postal_code,expected", [
        ("张三", "李四", "100000", True),
        ("", "李四", "100000", False),  # 缺少名字
        ("张三", "", "100000", False),  # 缺少姓氏
        ("张三", "李四", "", False),     # 缺少邮编
        ("Test", "User", "12345", True),  # 英文信息
    ])
    @allure.story("参数化测试结算信息")
    def test_checkout_with_parameters(self, first_name, last_name, postal_code, expected):
        """使用参数化测试不同的结算信息组合"""
        with allure.step(f"测试信息: {first_name} {last_name} {postal_code}"):
            self.cart_page.click_checkout()
            self.checkout_page.enter_checkout_info(first_name, last_name, postal_code)
            self.checkout_page.click_continue()
            
            if expected:
                # 应该成功进入第二步
                assert "checkout-step-two.html" in self.driver.current_url
                self.checkout_page.click_cancel()  # 取消，不实际完成订单
            else:
                # 应该显示错误信息
                error_message = self.checkout_page.get_error_message()
                assert error_message is not None
                assert "required" in error_message.lower()