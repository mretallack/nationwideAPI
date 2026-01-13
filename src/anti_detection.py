"""Anti-detection and bot evasion"""

import random
import time
import string
from typing import List, Tuple
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.webelement import WebElement
import logging

logger = logging.getLogger(__name__)

class AntiDetection:
    """Anti-detection utilities for browser automation"""
    
    # Common user agents for rotation
    USER_AGENTS = [
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    ]
    
    @staticmethod
    def random_delay(min_seconds: float = 1.0, max_seconds: float = 3.0):
        """Add random delay to mimic human behavior"""
        delay = random.uniform(min_seconds, max_seconds)
        logger.debug(f"Random delay: {delay:.2f}s")
        time.sleep(delay)
    
    @staticmethod
    def typing_delay() -> float:
        """Get random typing delay between characters"""
        return random.uniform(0.05, 0.15)
    
    @staticmethod
    def get_random_user_agent() -> str:
        """Get random user agent string"""
        return random.choice(AntiDetection.USER_AGENTS)
    
    @staticmethod
    def human_like_typing(element: WebElement, text: str, driver=None):
        """Type text with human-like delays and occasional mistakes"""
        try:
            # Clear existing text
            element.clear()
            AntiDetection.random_delay(0.2, 0.5)
            
            # Type character by character
            for i, char in enumerate(text):
                element.send_keys(char)
                
                # Random typing delay
                time.sleep(AntiDetection.typing_delay())
                
                # Occasional pause (like thinking)
                if random.random() < 0.1:  # 10% chance
                    time.sleep(random.uniform(0.3, 0.8))
                
                # Very rare typo simulation (disabled for credentials)
                # if random.random() < 0.02 and i < len(text) - 1:
                #     wrong_char = random.choice(string.ascii_lowercase)
                #     element.send_keys(wrong_char)
                #     time.sleep(0.1)
                #     element.send_keys('\b')  # Backspace
            
            logger.debug(f"Typed text with human-like behavior: {len(text)} characters")
            
        except Exception as e:
            logger.error(f"Human-like typing failed: {e}")
            # Fallback to normal typing
            element.clear()
            element.send_keys(text)
    
    @staticmethod
    def random_mouse_movement(driver, element: WebElement = None):
        """Add random mouse movements"""
        try:
            actions = ActionChains(driver)
            
            if element:
                # Move to element with slight randomness
                actions.move_to_element_with_offset(
                    element, 
                    random.randint(-5, 5), 
                    random.randint(-5, 5)
                )
            else:
                # Random movement within viewport
                actions.move_by_offset(
                    random.randint(-100, 100),
                    random.randint(-100, 100)
                )
            
            actions.perform()
            AntiDetection.random_delay(0.1, 0.3)
            
        except Exception as e:
            logger.debug(f"Mouse movement failed: {e}")
    
    @staticmethod
    def scroll_randomly(driver):
        """Add random scrolling behavior"""
        try:
            # Random scroll amount
            scroll_amount = random.randint(100, 500)
            direction = random.choice([-1, 1])
            
            driver.execute_script(f"window.scrollBy(0, {scroll_amount * direction});")
            AntiDetection.random_delay(0.5, 1.5)
            
        except Exception as e:
            logger.debug(f"Random scroll failed: {e}")
    
    @staticmethod
    def get_chrome_options():
        """Get Chrome options with anti-detection settings"""
        from selenium.webdriver.chrome.options import Options
        
        options = Options()
        
        # Basic anti-detection
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        # Additional stealth options
        options.add_argument("--disable-extensions")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-features=VizDisplayCompositor")
        
        # Random user agent
        user_agent = AntiDetection.get_random_user_agent()
        options.add_argument(f"--user-agent={user_agent}")
        
        # Window size variation
        width = random.randint(1200, 1920)
        height = random.randint(800, 1080)
        options.add_argument(f"--window-size={width},{height}")
        
        return options
    
    @staticmethod
    def setup_stealth_driver(driver):
        """Apply additional stealth measures to driver"""
        try:
            # Remove webdriver property
            driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            # Override plugins length
            driver.execute_script("Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]})")
            
            # Override languages
            driver.execute_script("Object.defineProperty(navigator, 'languages', {get: () => ['en-US', 'en']})")
            
            logger.debug("Stealth measures applied to driver")
            
        except Exception as e:
            logger.error(f"Failed to apply stealth measures: {e}")
    
    @staticmethod
    def wait_for_human_verification(message: str = "Please complete any verification and press Enter..."):
        """Pause for manual human intervention"""
        print(f"\n🔐 {message}")
        input("Press Enter to continue...")
        logger.info("Human verification completed")

class BehaviorPattern:
    """Simulate realistic browsing patterns"""
    
    def __init__(self, driver):
        self.driver = driver
        self.anti_detection = AntiDetection()
    
    def simulate_reading(self, min_seconds: float = 2.0, max_seconds: float = 5.0):
        """Simulate reading page content"""
        # Random scroll and pause pattern
        for _ in range(random.randint(1, 3)):
            self.anti_detection.scroll_randomly(self.driver)
            self.anti_detection.random_delay(min_seconds/3, max_seconds/3)
        
        # Final pause as if reading
        self.anti_detection.random_delay(min_seconds, max_seconds)
    
    def simulate_form_interaction(self, form_elements: List[WebElement]):
        """Simulate realistic form interaction"""
        for element in form_elements:
            # Move mouse to element
            self.anti_detection.random_mouse_movement(self.driver, element)
            
            # Small pause before interaction
            self.anti_detection.random_delay(0.3, 0.8)
            
            # Click element
            element.click()
            
            # Pause after click
            self.anti_detection.random_delay(0.2, 0.5)
