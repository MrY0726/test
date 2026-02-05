from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import Config

class LoginPage:
    """登录页面对象模型"""
    
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, Config.EXPLICIT_WAIT)
        
    # 元素定位器
    USERNAME_INPUT = (By.ID, "user-name")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "h3[data-test='error']")
    PRODUCTS_TITLE = (By.CLASS_NAME, "title")
    
    def open(self):
        """打开登录页面"""
        self.driver.get(Config.BASE_URL)
        return self
    
    def enter_username(self, username):
        """输入用户名"""
        self.wait.until(EC.presence_of_element_located(self.USERNAME_INPUT))
        self.driver.find_element(*self.USERNAME_INPUT).clear()
        self.driver.find_element(*self.USERNAME_INPUT).send_keys(username)
        return self
    
    def enter_password(self, password):
        """输入密码"""
        self.driver.find_element(*self.PASSWORD_INPUT).clear()
        self.driver.find_element(*self.PASSWORD_INPUT).send_keys(password)
        return self
    
    def click_login(self):
        """点击登录按钮"""
        self.driver.find_element(*self.LOGIN_BUTTON).click()
        return self
    
    def login(self, username, password):
        """完整的登录流程"""
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()
        return self
    
    def get_error_message(self):
        """获取错误信息"""
        try:
            return self.driver.find_element(*self.ERROR_MESSAGE).text
        except:
            return None
    
    def is_login_successful(self):
        """验证是否登录成功"""
        try:
            self.wait.until(EC.presence_of_element_located(self.PRODUCTS_TITLE))
            return True
        except:
            return False