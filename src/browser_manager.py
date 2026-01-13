"""Browser automation manager"""

import logging
import time
from typing import Optional, Dict, Any, List
from selenium import webdriver
from seleniumwire import webdriver as wire_webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
import undetected_chromedriver as uc

from .anti_detection import AntiDetection, BehaviorPattern
from .config import config

logger = logging.getLogger(__name__)

class BrowserManager:
    """Manages browser automation with anti-detection and network monitoring"""
    
    def __init__(self, capture_traffic: bool = False):
        self.driver: Optional[webdriver.Chrome] = None
        self.capture_traffic = capture_traffic
        self.behavior = None
        self.anti_detection = AntiDetection()
        
    def start_browser(self) -> bool:
        """Start browser with anti-detection measures"""
        try:
            logger.info("Starting browser...")
            
            # Get configuration
            headless = config.getboolean('browser', 'headless', False)
            timeout = config.getint('browser', 'timeout', 30)
            window_size = config.get('browser', 'window_size', '1920x1080')
            
            # Setup Chrome options
            options = self.anti_detection.get_chrome_options()
            
            if headless:
                options.add_argument('--headless')
                logger.info("Running in headless mode")
            
            # Set window size
            options.add_argument(f'--window-size={window_size}')
            
            # User data directory for session persistence
            user_data_dir = config.get('browser', 'user_data_dir', '~/.nationwide-cli/browser')
            options.add_argument(f'--user-data-dir={user_data_dir}')
            
            # Create driver with or without traffic capture
            if self.capture_traffic:
                logger.info("Starting browser with network monitoring")
                # Use selenium-wire for traffic capture
                wire_options = {
                    'disable_encoding': True,  # Don't decode responses
                    'suppress_connection_errors': False,
                }
                self.driver = wire_webdriver.Chrome(options=options, seleniumwire_options=wire_options)
            else:
                logger.info("Starting browser with undetected-chromedriver")
                # Use undetected-chromedriver for better stealth
                self.driver = uc.Chrome(options=options, version_main=None)
            
            # Apply stealth measures
            self.anti_detection.setup_stealth_driver(self.driver)
            
            # Set timeouts
            self.driver.implicitly_wait(timeout)
            self.driver.set_page_load_timeout(timeout)
            
            # Initialize behavior pattern
            self.behavior = BehaviorPattern(self.driver)
            
            logger.info("Browser started successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to start browser: {e}")
            self.cleanup()
            return False
    
    def navigate_to_login(self) -> bool:
        """Navigate to Nationwide login page"""
        try:
            base_url = config.get('nationwide', 'base_url', 'https://onlinebanking.nationwide.co.uk')
            logger.info(f"Navigating to {base_url}")
            
            self.driver.get(base_url)
            
            # Wait for page to load
            self.anti_detection.random_delay(2, 4)
            
            # Simulate reading the page
            self.behavior.simulate_reading(3, 6)
            
            logger.info(f"Successfully navigated to login page")
            logger.info(f"Page title: {self.driver.title}")
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to navigate to login page: {e}")
            return False
    
    def find_login_form(self) -> Dict[str, Any]:
        """Find and analyze login form elements"""
        try:
            logger.info("Analyzing login form...")
            
            # Common selectors for login forms
            username_selectors = [
                'input[name="username"]',
                'input[name="customerNumber"]', 
                'input[id="username"]',
                'input[id="customer-number"]',
                'input[type="text"]',
            ]
            
            password_selectors = [
                'input[type="password"]',
                'input[name="password"]',
                'input[id="password"]',
            ]
            
            submit_selectors = [
                'input[type="submit"]',
                'button[type="submit"]',
                'button:contains("Log in")',
                'button:contains("Sign in")',
            ]
            
            form_info = {
                'username_field': None,
                'password_field': None,
                'submit_button': None,
                'form_found': False
            }
            
            # Find username field
            for selector in username_selectors:
                try:
                    element = self.driver.find_element(By.CSS_SELECTOR, selector)
                    if element.is_displayed():
                        form_info['username_field'] = element
                        logger.info(f"Found username field: {selector}")
                        break
                except:
                    continue
            
            # Find password field
            for selector in password_selectors:
                try:
                    element = self.driver.find_element(By.CSS_SELECTOR, selector)
                    if element.is_displayed():
                        form_info['password_field'] = element
                        logger.info(f"Found password field: {selector}")
                        break
                except:
                    continue
            
            # Find submit button
            for selector in submit_selectors:
                try:
                    element = self.driver.find_element(By.CSS_SELECTOR, selector)
                    if element.is_displayed():
                        form_info['submit_button'] = element
                        logger.info(f"Found submit button: {selector}")
                        break
                except:
                    continue
            
            # Check if we found a complete form
            if form_info['username_field'] and form_info['password_field']:
                form_info['form_found'] = True
                logger.info("✓ Complete login form found")
            else:
                logger.warning("⚠ Incomplete login form - may need JavaScript to load")
                
                # Wait a bit more for dynamic content
                self.anti_detection.random_delay(3, 5)
                
                # Try again after waiting
                return self.find_login_form()
            
            return form_info
            
        except Exception as e:
            logger.error(f"Failed to analyze login form: {e}")
            return {'form_found': False}
    
    def attempt_login(self, username: str, password: str) -> bool:
        """Attempt to login with provided credentials"""
        try:
            logger.info("Attempting login...")
            
            # Find login form
            form_info = self.find_login_form()
            if not form_info['form_found']:
                logger.error("Login form not found")
                return False
            
            # Fill username
            if form_info['username_field']:
                logger.info("Filling username field")
                self.anti_detection.human_like_typing(form_info['username_field'], username)
                self.anti_detection.random_delay(1, 2)
            
            # Fill password
            if form_info['password_field']:
                logger.info("Filling password field")
                self.anti_detection.human_like_typing(form_info['password_field'], password)
                self.anti_detection.random_delay(1, 2)
            
            # Submit form
            if form_info['submit_button']:
                logger.info("Submitting login form")
                self.anti_detection.random_mouse_movement(self.driver, form_info['submit_button'])
                self.anti_detection.random_delay(0.5, 1.0)
                form_info['submit_button'].click()
            else:
                # Try form submission via Enter key
                logger.info("Submitting via Enter key")
                form_info['password_field'].send_keys('\n')
            
            # Wait for response
            self.anti_detection.random_delay(3, 5)
            
            # Check for MFA or success
            return self.check_login_result()
            
        except Exception as e:
            logger.error(f"Login attempt failed: {e}")
            return False
    
    def check_login_result(self) -> bool:
        """Check the result of login attempt"""
        try:
            current_url = self.driver.current_url
            page_source = self.driver.page_source.lower()
            
            logger.info(f"Current URL after login: {current_url}")
            
            # Check for success indicators
            success_indicators = [
                'dashboard', 'account', 'balance', 'welcome', 'overview'
            ]
            
            # Check for MFA indicators
            mfa_indicators = [
                'verification', 'code', 'authenticate', 'security', 'sms', 'mobile'
            ]
            
            # Check for error indicators
            error_indicators = [
                'error', 'incorrect', 'invalid', 'failed', 'blocked'
            ]
            
            if any(indicator in page_source for indicator in success_indicators):
                logger.info("✓ Login appears successful")
                return True
            elif any(indicator in page_source for indicator in mfa_indicators):
                logger.info("🔐 MFA required - waiting for user intervention")
                self.anti_detection.wait_for_human_verification(
                    "Please complete MFA verification and press Enter..."
                )
                return self.check_login_result()  # Check again after MFA
            elif any(indicator in page_source for indicator in error_indicators):
                logger.error("✗ Login failed - error detected")
                return False
            else:
                logger.warning("⚠ Login result unclear - may need manual verification")
                return False
                
        except Exception as e:
            logger.error(f"Failed to check login result: {e}")
            return False
    
    def get_network_requests(self) -> List[Dict[str, Any]]:
        """Get captured network requests (only if traffic capture enabled)"""
        if not self.capture_traffic or not hasattr(self.driver, 'requests'):
            return []
        
        requests = []
        for request in self.driver.requests:
            if request.response:
                requests.append({
                    'url': request.url,
                    'method': request.method,
                    'status_code': request.response.status_code,
                    'headers': dict(request.headers),
                    'response_headers': dict(request.response.headers),
                })
        
        return requests
    
    def save_page_source(self, filename: str = None):
        """Save current page source for analysis"""
        if not filename:
            import datetime
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"/tmp/nationwide_page_{timestamp}.html"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(self.driver.page_source)
            logger.info(f"Page source saved to {filename}")
        except Exception as e:
            logger.error(f"Failed to save page source: {e}")
    
    def cleanup(self):
        """Clean up browser resources"""
        try:
            if self.driver:
                self.driver.quit()
                self.driver = None
                logger.info("Browser cleaned up")
        except Exception as e:
            logger.error(f"Error during cleanup: {e}")
    
    def __enter__(self):
        """Context manager entry"""
        if self.start_browser():
            return self
        else:
            raise RuntimeError("Failed to start browser")
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.cleanup()
