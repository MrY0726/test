from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import Config

class CartPage:
    """购物车页面"""
    
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, Config.EXPLICIT_WAIT)
    
    # 元素定位器
    CART_ITEMS = (By.CLASS_NAME, "cart_item")
    CHECKOUT_BUTTON = (By.ID, "checkout")
    
    def get_cart_items_count(self):
        """获取购物车中商品数量"""
        return len(self.driver.find_elements(*self.CART_ITEMS))
    
    def click_checkout(self):
        """点击结算按钮"""
        self.wait.until(EC.element_to_be_clickable(self.CHECKOUT_BUTTON)).click()