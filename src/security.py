"""Security and encryption utilities"""

import os
import json
import keyring
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
from typing import Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)

class SecurityManager:
    """Handles encryption and secure storage"""
    
    def __init__(self, key_name: str = "nationwide_cli_key"):
        self.key_name = key_name
        self.service_name = "nationwide-balance-viewer"
        self._fernet = None
    
    def _get_or_create_key(self) -> bytes:
        """Get encryption key from keyring or create new one"""
        try:
            # Try to get existing key
            key_str = keyring.get_password(self.service_name, self.key_name)
            if key_str:
                return base64.urlsafe_b64decode(key_str.encode())
            
            # Create new key
            key = Fernet.generate_key()
            key_str = base64.urlsafe_b64encode(key).decode()
            keyring.set_password(self.service_name, self.key_name, key_str)
            logger.info("Created new encryption key")
            return key
            
        except Exception as e:
            logger.error(f"Failed to manage encryption key: {e}")
            # Fallback to session-only key (not persistent)
            logger.warning("Using session-only encryption key")
            return Fernet.generate_key()
    
    def _get_fernet(self) -> Fernet:
        """Get Fernet encryption instance"""
        if self._fernet is None:
            key = self._get_or_create_key()
            self._fernet = Fernet(key)
        return self._fernet
    
    def encrypt_data(self, data: Any) -> str:
        """Encrypt data and return base64 string"""
        try:
            # Convert to JSON string
            json_str = json.dumps(data)
            
            # Encrypt
            fernet = self._get_fernet()
            encrypted = fernet.encrypt(json_str.encode())
            
            # Return base64 encoded
            return base64.urlsafe_b64encode(encrypted).decode()
            
        except Exception as e:
            logger.error(f"Encryption failed: {e}")
            raise
    
    def decrypt_data(self, encrypted_str: str) -> Any:
        """Decrypt base64 string and return data"""
        try:
            # Decode base64
            encrypted = base64.urlsafe_b64decode(encrypted_str.encode())
            
            # Decrypt
            fernet = self._get_fernet()
            decrypted = fernet.decrypt(encrypted)
            
            # Parse JSON
            return json.loads(decrypted.decode())
            
        except Exception as e:
            logger.error(f"Decryption failed: {e}")
            raise
    
    def clear_stored_key(self):
        """Remove encryption key from keyring"""
        try:
            keyring.delete_password(self.service_name, self.key_name)
            self._fernet = None
            logger.info("Encryption key cleared")
        except Exception as e:
            logger.error(f"Failed to clear encryption key: {e}")

class SessionStorage:
    """Secure session data storage"""
    
    def __init__(self, storage_dir: str = None):
        self.storage_dir = storage_dir or os.path.expanduser("~/.nationwide-cli")
        self.session_file = os.path.join(self.storage_dir, "session.enc")
        self.security = SecurityManager()
        
        # Ensure storage directory exists
        os.makedirs(self.storage_dir, mode=0o700, exist_ok=True)
    
    def save_session(self, session_data: Dict[str, Any]):
        """Save encrypted session data"""
        try:
            encrypted_data = self.security.encrypt_data(session_data)
            
            with open(self.session_file, 'w') as f:
                f.write(encrypted_data)
            
            # Set restrictive permissions
            os.chmod(self.session_file, 0o600)
            logger.info("Session data saved securely")
            
        except Exception as e:
            logger.error(f"Failed to save session: {e}")
            raise
    
    def load_session(self) -> Optional[Dict[str, Any]]:
        """Load and decrypt session data"""
        try:
            if not os.path.exists(self.session_file):
                return None
            
            with open(self.session_file, 'r') as f:
                encrypted_data = f.read()
            
            session_data = self.security.decrypt_data(encrypted_data)
            logger.info("Session data loaded successfully")
            return session_data
            
        except Exception as e:
            logger.error(f"Failed to load session: {e}")
            # Remove corrupted session file
            self.clear_session()
            return None
    
    def clear_session(self):
        """Remove session file"""
        try:
            if os.path.exists(self.session_file):
                os.remove(self.session_file)
                logger.info("Session data cleared")
        except Exception as e:
            logger.error(f"Failed to clear session: {e}")
    
    def session_exists(self) -> bool:
        """Check if session file exists"""
        return os.path.exists(self.session_file)

def secure_cleanup():
    """Clean up all sensitive data"""
    try:
        # Clear session storage
        storage = SessionStorage()
        storage.clear_session()
        
        # Clear encryption key
        security = SecurityManager()
        security.clear_stored_key()
        
        logger.info("Secure cleanup completed")
        
    except Exception as e:
        logger.error(f"Secure cleanup failed: {e}")

# Global instances
session_storage = SessionStorage()
security_manager = SecurityManager()
