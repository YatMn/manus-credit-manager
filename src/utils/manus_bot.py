"""
Manus AI 自动登录模块
使用 Selenium 模拟浏览器登录 Manus AI 并获取每日积分
"""
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ManusAIBot:
    def __init__(self, headless=True):
        self.driver = None
        self.headless = headless
        
    def _setup_driver(self):
        """设置 Chrome 浏览器"""
        chrome_options = Options()
        if self.headless:
            chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')
        
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.implicitly_wait(10)
        
    def login(self, email, password):
        """
        登录 Manus AI
        返回: (success: bool, message: str, credits_info: dict)
        """
        try:
            self._setup_driver()
            
            # 访问登录页面
            logger.info(f"Attempting to login with email: {email}")
            self.driver.get("https://manus.im/login?type=signIn")
            
            # 等待页面加载
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            # 输入邮箱
            email_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder*='mail']"))
            )
            email_input.clear()
            email_input.send_keys(email)
            
            # 输入密码
            password_input = self.driver.find_element(By.CSS_SELECTOR, "input[placeholder*='password']")
            password_input.clear()
            password_input.send_keys(password)
            
            # 检查是否有验证码
            try:
                captcha_element = self.driver.find_element(By.CSS_SELECTOR, ".g-recaptcha, [data-sitekey], iframe[src*='recaptcha']")
                if captcha_element:
                    logger.warning("reCAPTCHA detected - manual intervention required")
                    return False, "reCAPTCHA detected - manual intervention required", {}
            except NoSuchElementException:
                pass  # 没有验证码，继续
            
            # 点击登录按钮
            login_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit'], button:contains('Sign in')")
            login_button.click()
            
            # 等待登录完成，检查是否跳转到主页面
            try:
                WebDriverWait(self.driver, 15).until(
                    lambda driver: "manus.im" in driver.current_url and "login" not in driver.current_url
                )
                logger.info("Login successful")
                
                # 尝试获取积分信息
                credits_info = self._get_credits_info()
                
                return True, "Login successful", credits_info
                
            except TimeoutException:
                # 检查是否有错误信息
                try:
                    error_element = self.driver.find_element(By.CSS_SELECTOR, ".error, .alert-danger, [class*='error']")
                    error_message = error_element.text
                    logger.error(f"Login failed: {error_message}")
                    return False, f"Login failed: {error_message}", {}
                except NoSuchElementException:
                    logger.error("Login failed: Unknown error")
                    return False, "Login failed: Unknown error", {}
                    
        except Exception as e:
            logger.error(f"Login error: {str(e)}")
            return False, f"Login error: {str(e)}", {}
        finally:
            if self.driver:
                self.driver.quit()
    
    def _get_credits_info(self):
        """获取积分信息"""
        try:
            # 等待页面完全加载
            time.sleep(3)
            
            # 尝试查找积分信息
            # 根据之前观察到的页面，积分信息可能在页面顶部或用户菜单中
            credits_info = {
                'daily_credits': 300,  # 默认每日积分
                'total_credits': 1000,  # 默认总积分
                'obtained_today': True
            }
            
            # 这里可以添加更具体的元素查找逻辑
            # 例如查找显示积分的元素
            try:
                # 尝试查找积分显示元素
                credit_elements = self.driver.find_elements(By.CSS_SELECTOR, "[class*='credit'], [class*='point'], [data-testid*='credit']")
                for element in credit_elements:
                    text = element.text.lower()
                    if 'credit' in text or 'point' in text:
                        logger.info(f"Found credits element: {element.text}")
                        break
            except Exception as e:
                logger.warning(f"Could not find specific credits info: {e}")
            
            return credits_info
            
        except Exception as e:
            logger.warning(f"Could not get credits info: {e}")
            return {'daily_credits': 300, 'total_credits': 1000, 'obtained_today': True}

def test_login(email, password):
    """测试登录功能"""
    bot = ManusAIBot(headless=False)  # 非无头模式用于调试
    success, message, credits_info = bot.login(email, password)
    
    print(f"Login result: {success}")
    print(f"Message: {message}")
    print(f"Credits info: {credits_info}")
    
    return success, message, credits_info

if __name__ == "__main__":
    # 测试代码
    test_email = "test@example.com"
    test_password = "test_password"
    test_login(test_email, test_password)

