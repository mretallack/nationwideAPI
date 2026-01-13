"""Test anti-detection utilities"""

import pytest
import time
from unittest.mock import Mock, MagicMock
from src.anti_detection import AntiDetection, BehaviorPattern

class TestAntiDetection:
    def test_random_delay(self):
        """Test random delay functionality"""
        start_time = time.time()
        AntiDetection.random_delay(0.1, 0.2)
        end_time = time.time()
        
        elapsed = end_time - start_time
        assert 0.1 <= elapsed <= 0.3  # Allow some tolerance
    
    def test_typing_delay(self):
        """Test typing delay range"""
        delay = AntiDetection.typing_delay()
        assert 0.05 <= delay <= 0.15
    
    def test_user_agent_rotation(self):
        """Test user agent rotation"""
        user_agents = set()
        for _ in range(10):
            ua = AntiDetection.get_random_user_agent()
            user_agents.add(ua)
            assert "Mozilla" in ua
            assert "Chrome" in ua
        
        # Should get some variety (not all the same)
        assert len(user_agents) > 1
    
    def test_human_like_typing(self):
        """Test human-like typing simulation"""
        mock_element = Mock()
        mock_element.clear = Mock()
        mock_element.send_keys = Mock()
        
        test_text = "test123"
        AntiDetection.human_like_typing(mock_element, test_text)
        
        # Verify element was cleared
        mock_element.clear.assert_called_once()
        
        # Verify send_keys was called for each character
        assert mock_element.send_keys.call_count >= len(test_text)
    
    def test_chrome_options(self):
        """Test Chrome options configuration"""
        options = AntiDetection.get_chrome_options()
        
        # Check that options object is created
        assert options is not None
        
        # Verify some arguments are set (can't easily test all without Chrome)
        arguments = options.arguments
        assert any("--disable-blink-features=AutomationControlled" in arg for arg in arguments)
        assert any("--user-agent=" in arg for arg in arguments)
        assert any("--window-size=" in arg for arg in arguments)
    
    def test_stealth_driver_setup(self):
        """Test stealth driver setup"""
        mock_driver = Mock()
        mock_driver.execute_script = Mock()
        
        AntiDetection.setup_stealth_driver(mock_driver)
        
        # Verify execute_script was called multiple times for stealth setup
        assert mock_driver.execute_script.call_count >= 3

class TestBehaviorPattern:
    def test_behavior_pattern_creation(self):
        """Test behavior pattern initialization"""
        mock_driver = Mock()
        pattern = BehaviorPattern(mock_driver)
        
        assert pattern.driver == mock_driver
        assert pattern.anti_detection is not None
    
    def test_simulate_form_interaction(self):
        """Test form interaction simulation"""
        mock_driver = Mock()
        mock_element1 = Mock()
        mock_element2 = Mock()
        
        pattern = BehaviorPattern(mock_driver)
        pattern.simulate_form_interaction([mock_element1, mock_element2])
        
        # Verify elements were clicked
        mock_element1.click.assert_called_once()
        mock_element2.click.assert_called_once()
