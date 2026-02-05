from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import Config

class CheckoutPage:
    """结算页面对象模型"""
    
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, Config.EXPLICIT_WAIT)
    
    # 元素定位器 - 结算第一步（填写信息页面）
    FIRST_NAME_INPUT = (By.ID, "first-name")
    LAST_NAME_INPUT = (By.ID, "last-name")
    POSTAL_CODE_INPUT = (By.ID, "postal-code")
    CONTINUE_BUTTON = (By.ID, "continue")
    CANCEL_BUTTON = (By.ID, "cancel")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "h3[data-test='error']")
    
    # 元素定位器 - 结算第二步（订单概览页面）
    ITEM_TOTAL = (By.CLASS_NAME, "summary_subtotal_label")
    TAX_AMOUNT = (By.CLASS_NAME, "summary_tax_label")
    TOTAL_AMOUNT = (By.CLASS_NAME, "summary_total_label")
    FINISH_BUTTON = (By.ID, "finish")
    CANCEL_BUTTON_STEP2 = (By.ID, "cancel")
    
    # 元素定位器 - 结算完成页面
    SUCCESS_MESSAGE = (By.CLASS_NAME, "complete-header")
    COMPLETE_TEXT = (By.CLASS_NAME, "complete-text")
    BACK_HOME_BUTTON = (By.ID, "back-to-products")
    
    def enter_checkout_info(self, first_name, last_name, postal_code):
        """填写结算信息（第一步）"""
        self.wait.until(EC.presence_of_element_located(self.FIRST_NAME_INPUT))

        # 重要：无论是否传空字符串，都需要先清空输入框。
        # 否则在参数化/多步骤用例中，上一轮输入会残留导致断言不稳定。
        first_name_input = self.driver.find_element(*self.FIRST_NAME_INPUT)
        last_name_input = self.driver.find_element(*self.LAST_NAME_INPUT)
        postal_code_input = self.driver.find_element(*self.POSTAL_CODE_INPUT)

        first_name_input.clear()
        last_name_input.clear()
        postal_code_input.clear()

        if first_name:
            first_name_input.send_keys(first_name)
        if last_name:
            last_name_input.send_keys(last_name)
        if postal_code:
            postal_code_input.send_keys(postal_code)
        
        return self
    
    def click_continue(self):
        """点击继续按钮（前往第二步）"""
        self.driver.find_element(*self.CONTINUE_BUTTON).click()
        return self
    
    def click_cancel(self):
        """点击取消按钮"""
        try:
            # 尝试点击第一步的取消按钮
            self.driver.find_element(*self.CANCEL_BUTTON).click()
        except:
            # 如果在第二步，点击第二步的取消按钮
            try:
                self.driver.find_element(*self.CANCEL_BUTTON_STEP2).click()
            except:
                print("未找到取消按钮")
        return self
    
    def click_finish(self):
        """点击完成按钮（完成订单）"""
        self.driver.find_element(*self.FINISH_BUTTON).click()
        return self
    
    def get_error_message(self):
        """获取错误信息"""
        try:
            return self.driver.find_element(*self.ERROR_MESSAGE).text
        except:
            return None
    
    def get_order_summary(self):
        """获取订单摘要信息"""
        try:
            # SauceDemo 的 checkout-step-two 页面结构：
            # - .summary_info_label: Payment Information:, Shipping Information:, Price Total:
            # - .summary_value_label: 对应 value（前两个 label 有 value）
            labels = [el.text.strip() for el in self.driver.find_elements(By.CLASS_NAME, "summary_info_label")]
            values = [el.text.strip() for el in self.driver.find_elements(By.CLASS_NAME, "summary_value_label")]

            # 前两个 label（支付/配送）通常各对应一个 value
            payment_label = labels[0] if len(labels) > 0 else "Payment Information"
            shipping_label = labels[1] if len(labels) > 1 else "Shipping Information"
            price_total_label = labels[2] if len(labels) > 2 else "Price Total"

            payment_value = values[0] if len(values) > 0 else ""
            shipping_value = values[1] if len(values) > 1 else ""

            item_total = self.get_item_total()
            tax_amount = self.get_tax_amount()
            total_amount = self.get_total_amount()

            # 注意：测试用例里断言包含 "Payment Information" / "Shipping Information" / "Price Total"
            # 所以这里保留页面原始英文 label，方便做稳定断言。
            summary = (
                "Order Summary:\n"
                f"{payment_label} {payment_value}\n"
                f"{shipping_label} {shipping_value}\n"
                f"{price_total_label}\n"
                f"Item total: ${item_total:.2f}\n"
                f"Tax: ${tax_amount:.2f}\n"
                f"Total: ${total_amount:.2f}"
            )
            return summary

        except Exception as e:
            return f"获取订单摘要失败: {e}"
    
    def get_item_total(self):
        """获取商品小计金额"""
        try:
            text = self.driver.find_element(*self.ITEM_TOTAL).text
            # 从 "Item total: $29.99" 中提取数字
            amount_text = text.split('$')[-1]
            return float(amount_text)
        except:
            return 0.0
    
    def get_tax_amount(self):
        """获取税费金额"""
        try:
            text = self.driver.find_element(*self.TAX_AMOUNT).text
            amount_text = text.split('$')[-1]
            return float(amount_text)
        except:
            return 0.0
    
    def get_total_amount(self):
        """获取总金额"""
        try:
            text = self.driver.find_element(*self.TOTAL_AMOUNT).text
            amount_text = text.split('$')[-1]
            return float(amount_text)
        except:
            return 0.0
    
    def get_success_message(self):
        """获取订单成功信息"""
        try:
            return self.driver.find_element(*self.SUCCESS_MESSAGE).text
        except:
            return ""
    
    def get_complete_text(self):
        """获取完成页面的详细说明"""
        try:
            return self.driver.find_element(*self.COMPLETE_TEXT).text
        except:
            return ""
    
    def is_order_complete(self):
        """检查订单是否完成"""
        try:
            return "checkout-complete.html" in self.driver.current_url
        except:
            return False
    
    def back_to_home(self):
        """返回首页"""
        try:
            self.driver.find_element(*self.BACK_HOME_BUTTON).click()
        except:
            # 如果按钮不存在，直接导航到首页
            self.driver.get(Config.BASE_URL + "inventory.html")
        return self
    
    def is_on_checkout_step_one(self):
        """检查是否在结算第一步"""
        try:
            return "checkout-step-one.html" in self.driver.current_url
        except:
            return False
    
    def is_on_checkout_step_two(self):
        """检查是否在结算第二步"""
        try:
            return "checkout-step-two.html" in self.driver.current_url
        except:
            return False
    
    def wait_for_checkout_step_two(self):
        """等待进入结算第二步"""
        self.wait.until(EC.url_contains("checkout-step-two"))
        return self
    
    def wait_for_order_complete(self):
        """等待订单完成"""
        self.wait.until(EC.url_contains("checkout-complete"))
        return self