"""Headless browser manager using requests-html"""

import logging
import time
from typing import Optional, Dict, Any, List
from requests_html import HTMLSession
from urllib.parse import urljoin, urlparse
import json

from .anti_detection import AntiDetection
from .config import config

logger = logging.getLogger(__name__)

class HeadlessBrowserManager:
    """Headless browser using requests-html (can execute JavaScript)"""
    
    def __init__(self, capture_traffic: bool = False):
        self.session = HTMLSession()
        self.capture_traffic = capture_traffic
        self.requests_log = []
        self.anti_detection = AntiDetection()
        self.base_url = config.get('nationwide', 'base_url', 'https://onlinebanking.nationwide.co.uk')
        
        # Setup realistic headers
        self.session.headers.update({
            'User-Agent': self.anti_detection.get_random_user_agent(),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-GB,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })
    
    def start_browser(self) -> bool:
        """Initialize headless browser session"""
        try:
            logger.info("Starting headless browser session...")
            
            # Test basic connectivity
            response = self.session.get(self.base_url)
            if response.status_code == 200:
                logger.info("✓ Headless browser session started successfully")
                return True
            else:
                logger.error(f"Failed to start session: {response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"Failed to start headless browser: {e}")
            return False
    
    def navigate_to_login(self) -> bool:
        """Navigate to login page and execute JavaScript"""
        try:
            logger.info(f"Navigating to {self.base_url}")
            
            # Get the page
            response = self.session.get(self.base_url)
            self._log_request(response)
            
            if response.status_code != 200:
                logger.error(f"Failed to load page: {response.status_code}")
                return False
            
            logger.info(f"✓ Page loaded: {response.status_code}")
            logger.info(f"✓ Content length: {len(response.content)} bytes")
            
            # Execute JavaScript to load dynamic content
            logger.info("Executing JavaScript to load dynamic content...")
            try:
                response.html.render(timeout=20, wait=3)
                logger.info("✓ JavaScript executed successfully")
            except Exception as e:
                logger.warning(f"JavaScript execution failed: {e}")
                logger.info("Continuing with static HTML...")
            
            # Check for redirect to login page
            if '/AccessManagement/Login' in response.url or 'login' in response.url.lower():
                logger.info("✓ Already on login page")
            else:
                # Try to find and follow login redirect
                login_redirect = self._find_login_redirect(response)
                if login_redirect:
                    logger.info(f"Following login redirect: {login_redirect}")
                    response = self.session.get(login_redirect)
                    self._log_request(response)
                    
                    # Execute JS on login page too
                    try:
                        response.html.render(timeout=20, wait=3)
                    except:
                        pass
            
            # Save page for analysis
            with open('/tmp/headless_login_page.html', 'w', encoding='utf-8') as f:
                f.write(response.html.html)
            logger.info("✓ Page saved to /tmp/headless_login_page.html")
            
            self.current_response = response
            return True
            
        except Exception as e:
            logger.error(f"Failed to navigate to login: {e}")
            return False
    
    def find_login_form(self) -> Dict[str, Any]:
        """Find login form elements in the current page"""
        try:
            logger.info("Analyzing login form...")
            
            if not hasattr(self, 'current_response'):
                logger.error("No current page loaded")
                return {'form_found': False}
            
            html = self.current_response.html
            
            # Look for forms
            forms = html.find('form')
            logger.info(f"Found {len(forms)} forms on page")
            
            form_info = {
                'username_field': None,
                'password_field': None,
                'submit_button': None,
                'form_found': False,
                'form_action': None
            }
            
            # Analyze each form
            for form in forms:
                # Get form action
                action = form.attrs.get('action', '')
                logger.info(f"Form action: {action}")
                
                # Look for input fields
                inputs = form.find('input')
                
                username_found = False
                password_found = False
                
                for input_elem in inputs:
                    input_type = input_elem.attrs.get('type', 'text').lower()
                    input_name = input_elem.attrs.get('name', '').lower()
                    input_id = input_elem.attrs.get('id', '').lower()
                    
                    # Check for username/customer number field
                    if (input_type in ['text', 'email'] or 
                        'customer' in input_name or 'user' in input_name or
                        'customer' in input_id or 'user' in input_id):
                        form_info['username_field'] = {
                            'name': input_elem.attrs.get('name'),
                            'id': input_elem.attrs.get('id'),
                            'type': input_type
                        }
                        username_found = True
                        logger.info(f"✓ Username field found: {input_name or input_id}")
                    
                    # Check for password field
                    elif input_type == 'password':
                        form_info['password_field'] = {
                            'name': input_elem.attrs.get('name'),
                            'id': input_elem.attrs.get('id'),
                            'type': input_type
                        }
                        password_found = True
                        logger.info(f"✓ Password field found: {input_name or input_id}")
                
                # If we found both username and password in this form
                if username_found and password_found:
                    form_info['form_found'] = True
                    form_info['form_action'] = action
                    logger.info("✓ Complete login form found")
                    break
            
            if not form_info['form_found']:
                logger.warning("⚠ Complete login form not found")
                # Log what we did find
                all_inputs = html.find('input')
                logger.info(f"All inputs found: {len(all_inputs)}")
                for inp in all_inputs[:10]:  # First 10
                    logger.info(f"  Input: type={inp.attrs.get('type')}, name={inp.attrs.get('name')}, id={inp.attrs.get('id')}")
            
            return form_info
            
        except Exception as e:
            logger.error(f"Failed to analyze login form: {e}")
            return {'form_found': False}
    
    def attempt_login(self, username: str, password: str) -> bool:
        """Attempt login using form submission"""
        try:
            logger.info("Attempting headless login...")
            
            form_info = self.find_login_form()
            if not form_info['form_found']:
                logger.error("Cannot login - no form found")
                return False
            
            # Prepare form data
            form_data = {}
            
            # Add username
            if form_info['username_field']:
                field_name = form_info['username_field']['name']
                if field_name:
                    form_data[field_name] = username
                    logger.info(f"Added username to field: {field_name}")
            
            # Add password
            if form_info['password_field']:
                field_name = form_info['password_field']['name']
                if field_name:
                    form_data[field_name] = password
                    logger.info(f"Added password to field: {field_name}")
            
            # Look for hidden fields (CSRF tokens, etc.)
            html = self.current_response.html
            hidden_inputs = html.find('input[type="hidden"]')
            for hidden in hidden_inputs:
                name = hidden.attrs.get('name')
                value = hidden.attrs.get('value')
                if name and value:
                    form_data[name] = value
                    logger.info(f"Added hidden field: {name}")
            
            # Determine form action URL
            form_action = form_info.get('form_action', '')
            if form_action:
                if form_action.startswith('/'):
                    login_url = urljoin(self.base_url, form_action)
                else:
                    login_url = form_action
            else:
                login_url = self.current_response.url
            
            logger.info(f"Submitting login to: {login_url}")
            logger.info(f"Form data fields: {list(form_data.keys())}")
            
            # Add delay to mimic human behavior
            self.anti_detection.random_delay(2, 4)
            
            # Submit the form
            response = self.session.post(login_url, data=form_data)
            self._log_request(response)
            
            # Check response
            if response.status_code in [200, 302]:
                logger.info(f"✓ Login submitted: {response.status_code}")
                
                # Execute JavaScript on response page
                try:
                    response.html.render(timeout=20, wait=3)
                except:
                    pass
                
                # Save response for analysis
                with open('/tmp/headless_after_login.html', 'w', encoding='utf-8') as f:
                    f.write(response.html.html)
                logger.info("✓ Post-login page saved to /tmp/headless_after_login.html")
                
                # Analyze response
                return self.check_login_result(response)
            else:
                logger.error(f"Login submission failed: {response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"Login attempt failed: {e}")
            return False
    
    def check_login_result(self, response) -> bool:
        """Check if login was successful"""
        try:
            content = response.html.html.lower()
            url = response.url.lower()
            
            logger.info(f"Checking login result for URL: {response.url}")
            
            # Success indicators
            success_indicators = [
                'dashboard', 'account', 'balance', 'welcome', 'overview', 'summary'
            ]
            
            # Error indicators
            error_indicators = [
                'error', 'incorrect', 'invalid', 'failed', 'blocked', 'denied'
            ]
            
            # MFA indicators
            mfa_indicators = [
                'verification', 'code', 'authenticate', 'security', 'sms', 'mobile'
            ]
            
            if any(indicator in content or indicator in url for indicator in success_indicators):
                logger.info("🎉 Login appears successful!")
                return True
            elif any(indicator in content for indicator in mfa_indicators):
                logger.info("🔐 MFA required (cannot handle in headless mode)")
                logger.info("This would require user interaction in a real browser")
                return False
            elif any(indicator in content for indicator in error_indicators):
                logger.error("❌ Login failed - error detected")
                return False
            else:
                logger.warning("⚠ Login result unclear")
                # Look for specific Nationwide indicators
                if 'nationwide' in content and ('login' not in content):
                    logger.info("✓ Appears to be logged in (on Nationwide page, no login form)")
                    return True
                return False
                
        except Exception as e:
            logger.error(f"Failed to check login result: {e}")
            return False
    
    def _find_login_redirect(self, response) -> Optional[str]:
        """Find login redirect URL in page content"""
        try:
            content = response.html.html
            
            # Look for JavaScript redirects
            if "window.location = '/AccessManagement/Login'" in content:
                return urljoin(self.base_url, '/AccessManagement/Login')
            
            # Look for meta redirects
            meta_refresh = response.html.find('meta[http-equiv="refresh"]')
            if meta_refresh:
                content_attr = meta_refresh[0].attrs.get('content', '')
                if 'url=' in content_attr:
                    url = content_attr.split('url=')[1]
                    return urljoin(self.base_url, url)
            
            return None
            
        except Exception as e:
            logger.error(f"Error finding login redirect: {e}")
            return None
    
    def _log_request(self, response):
        """Log request for traffic capture"""
        if self.capture_traffic:
            request_info = {
                'url': response.url,
                'method': 'GET' if not hasattr(response, 'request') else response.request.method,
                'status_code': response.status_code,
                'headers': dict(response.headers),
                'content_type': response.headers.get('content-type', ''),
            }
            self.requests_log.append(request_info)
    
    def get_network_requests(self) -> List[Dict[str, Any]]:
        """Get logged network requests"""
        return self.requests_log
    
    def cleanup(self):
        """Clean up session"""
        try:
            self.session.close()
            logger.info("Headless browser session closed")
        except Exception as e:
            logger.error(f"Error during cleanup: {e}")
    
    def __enter__(self):
        """Context manager entry"""
        if self.start_browser():
            return self
        else:
            raise RuntimeError("Failed to start headless browser")
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.cleanup()
