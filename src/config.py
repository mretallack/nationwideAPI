"""Configuration management"""

import os
import configparser
from pathlib import Path
from typing import Optional, Dict, Any

class Config:
    """Configuration manager for Nationwide Balance Viewer"""
    
    def __init__(self, config_file: Optional[str] = None):
        self.config_file = config_file or "settings.ini"
        self.config = configparser.ConfigParser()
        self.load_config()
    
    def load_config(self) -> None:
        """Load configuration from file"""
        if not os.path.exists(self.config_file):
            # Copy from template if settings.ini doesn't exist
            template_file = "settings.ini.template"
            if os.path.exists(template_file):
                import shutil
                shutil.copy(template_file, self.config_file)
                print(f"Created {self.config_file} from template")
            else:
                raise FileNotFoundError(f"Configuration file {self.config_file} not found")
        
        self.config.read(self.config_file)
    
    def get(self, section: str, key: str, fallback: Any = None) -> str:
        """Get configuration value"""
        return self.config.get(section, key, fallback=fallback)
    
    def getboolean(self, section: str, key: str, fallback: bool = False) -> bool:
        """Get boolean configuration value"""
        return self.config.getboolean(section, key, fallback=fallback)
    
    def getint(self, section: str, key: str, fallback: int = 0) -> int:
        """Get integer configuration value"""
        return self.config.getint(section, key, fallback=fallback)
    
    def get_section(self, section: str) -> Dict[str, str]:
        """Get entire configuration section"""
        if section in self.config:
            return dict(self.config[section])
        return {}

# Global config instance
config = Config()
