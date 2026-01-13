"""Test configuration management"""

import pytest
import tempfile
import os
from src.config import Config

class TestConfig:
    def test_config_loading(self):
        """Test configuration loading from template"""
        # Create temporary config file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.ini', delete=False) as f:
            f.write("""[DEFAULT]
debug = true
log_level = DEBUG

[browser]
headless = false
timeout = 30

[security]
session_timeout = 1800
""")
            temp_file = f.name
        
        try:
            config = Config(temp_file)
            assert config.getboolean('DEFAULT', 'debug') == True
            assert config.get('DEFAULT', 'log_level') == 'DEBUG'
            assert config.getint('browser', 'timeout') == 30
            assert config.getint('security', 'session_timeout') == 1800
        finally:
            os.unlink(temp_file)
    
    def test_config_sections(self):
        """Test getting entire configuration sections"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.ini', delete=False) as f:
            f.write("""[test_section]
key1 = value1
key2 = value2
""")
            temp_file = f.name
        
        try:
            config = Config(temp_file)
            section = config.get_section('test_section')
            assert section['key1'] == 'value1'
            assert section['key2'] == 'value2'
        finally:
            os.unlink(temp_file)
    
    def test_config_fallbacks(self):
        """Test configuration fallback values"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.ini', delete=False) as f:
            f.write("[empty]\n")
            temp_file = f.name
        
        try:
            config = Config(temp_file)
            assert config.get('empty', 'missing_key', 'default') == 'default'
            assert config.getboolean('empty', 'missing_bool', True) == True
            assert config.getint('empty', 'missing_int', 42) == 42
        finally:
            os.unlink(temp_file)
