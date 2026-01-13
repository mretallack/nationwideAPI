"""CLI interface for Nationwide Balance Viewer"""

import click
import logging
import getpass
from .browser_manager import BrowserManager
from .config import config

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@click.group()
@click.option('--debug', is_flag=True, help='Enable debug logging')
def cli(debug):
    """Nationwide Balance Viewer CLI"""
    if debug:
        logging.getLogger().setLevel(logging.DEBUG)
        logger.info("Debug logging enabled")

@cli.command()
def test_headless_navigation():
    """Test headless navigation to login page (no credentials needed)"""
    logger.info("Testing headless navigation to Nationwide...")
    
    try:
        from .headless_browser import HeadlessBrowserManager
        
        with HeadlessBrowserManager(capture_traffic=True) as browser:
            # Navigate to login page
            if browser.navigate_to_login():
                logger.info("✓ Successfully navigated to login page")
                
                # Analyze login form
                form_info = browser.find_login_form()
                if form_info['form_found']:
                    logger.info("✓ Login form found and analyzed")
                    logger.info(f"  - Username field: {form_info['username_field']}")
                    logger.info(f"  - Password field: {form_info['password_field']}")
                    logger.info(f"  - Form action: {form_info.get('form_action', 'Not specified')}")
                    
                    logger.info("\n🎯 Ready for login attempt!")
                    logger.info("The headless browser can:")
                    logger.info("- Navigate to Nationwide login page")
                    logger.info("- Execute JavaScript to load dynamic content")
                    logger.info("- Find and analyze login forms")
                    logger.info("- Submit forms with credentials")
                    logger.info("- Capture network traffic")
                    
                else:
                    logger.warning("⚠ Login form not found")
                
                # Show captured requests
                requests = browser.get_network_requests()
                logger.info(f"\n📊 Captured {len(requests)} network requests:")
                for req in requests[:5]:  # Show first 5
                    logger.info(f"  {req['method']} {req['url']} -> {req['status_code']}")
                
            else:
                logger.error("❌ Failed to navigate to login page")
                
    except Exception as e:
        logger.error(f"Headless navigation test failed: {e}")
        import traceback
        logger.error(traceback.format_exc())

@cli.command()
def config_info():
    """Show current configuration"""
    logger.info("Current configuration:")
    
    sections = ['DEFAULT', 'browser', 'security', 'debugging', 'nationwide']
    for section in sections:
        section_data = config.get_section(section)
        if section_data:
            logger.info(f"\n[{section}]")
            for key, value in section_data.items():
                # Hide sensitive values
                if 'password' in key.lower() or 'key' in key.lower():
                    value = '***'
                logger.info(f"  {key} = {value}")

def main():
    """Main entry point"""
    cli()

if __name__ == '__main__':
    main()
