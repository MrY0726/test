from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import Config

class HomePage:
    """首页/商品列表页面"""
    
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, Config.EXPLICIT_WAIT)
    
    # 元素定位器
    PRODUCTS_TITLE = (By.CLASS_NAME, "title")
    PRODUCT_ITEMS = (By.CLASS_NAME, "inventory_item")
    ADD_TO_CART_BUTTON = (By.CLASS_NAME, "btn_inventory")
    CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")
    CART_LINK = (By.CLASS_NAME, "shopping_cart_link")
    MENU_BUTTON = (By.ID, "react-burger-menu-btn")
    LOGOUT_LINK = (By.ID, "logout_sidebar_link")
    
    def get_page_title(self):
        """获取页面标题"""
        return self.driver.find_element(*self.PRODUCTS_TITLE).text
    
    def get_product_count(self):
        """获取商品数量"""
        return len(self.driver.find_elements(*self.PRODUCT_ITEMS))
    
    def add_first_product_to_cart(self):
        """添加第一个商品到购物车"""
        # 等待商品列表加载完成，避免偶发找不到按钮
        self.wait.until(EC.presence_of_all_elements_located(self.PRODUCT_ITEMS))
        add_buttons = self.driver.find_elements(*self.ADD_TO_CART_BUTTON)
        if add_buttons:
            add_buttons[0].click()
            return True
        return False

    def add_product_by_index(self, index: int) -> bool:
        """按索引添加商品到购物车（用于多商品场景）。

        SauceDemo 的每个商品卡片里都有一个 .btn_inventory 按钮。
        这里直接按按钮列表索引点击。
        """

        self.wait.until(EC.presence_of_all_elements_located(self.PRODUCT_ITEMS))
        add_buttons = self.driver.find_elements(*self.ADD_TO_CART_BUTTON)

        if 0 <= index < len(add_buttons):
            add_buttons[index].click()
            return True
        return False
    
    def get_cart_count(self):
        """获取购物车商品数量"""
        try:
            return int(self.driver.find_element(*self.CART_BADGE).text)
        except:
            return 0
    
    def go_to_cart(self):
        """前往购物车页面"""
        self.driver.find_element(*self.CART_LINK).click()
        # 等待购物车页面加载完成
        self.wait.until(EC.presence_of_element_located((By.ID, "checkout")))
        from pages.cart_page import CartPage
        return CartPage(self.driver)
    
    def logout(self):
        """登出"""
        self.driver.find_element(*self.MENU_BUTTON).click()
        self.wait.until(EC.element_to_be_clickable(self.LOGOUT_LINK)).click()