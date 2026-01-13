"""Test security utilities"""

import pytest
import tempfile
import os
from src.security import SecurityManager, SessionStorage

class TestSecurityManager:
    def test_encryption_decryption(self):
        """Test basic encryption and decryption"""
        security = SecurityManager("test_key")
        
        test_data = {
            "username": "testuser",
            "session_id": "abc123",
            "timestamp": "2024-01-01T12:00:00"
        }
        
        # Encrypt data
        encrypted = security.encrypt_data(test_data)
        assert isinstance(encrypted, str)
        assert len(encrypted) > 0
        
        # Decrypt data
        decrypted = security.decrypt_data(encrypted)
        assert decrypted == test_data
    
    def test_encryption_different_data_types(self):
        """Test encryption with different data types"""
        security = SecurityManager("test_key2")
        
        test_cases = [
            {"string": "test"},
            {"number": 123},
            {"boolean": True},
            {"list": [1, 2, 3]},
            {"nested": {"key": "value"}}
        ]
        
        for test_data in test_cases:
            encrypted = security.encrypt_data(test_data)
            decrypted = security.decrypt_data(encrypted)
            assert decrypted == test_data

class TestSessionStorage:
    def test_session_save_load(self):
        """Test session save and load"""
        with tempfile.TemporaryDirectory() as temp_dir:
            storage = SessionStorage(temp_dir)
            
            session_data = {
                "cookies": {"session": "abc123"},
                "user_agent": "test-agent",
                "timestamp": "2024-01-01T12:00:00"
            }
            
            # Save session
            storage.save_session(session_data)
            assert storage.session_exists()
            
            # Load session
            loaded_data = storage.load_session()
            assert loaded_data == session_data
    
    def test_session_clear(self):
        """Test session clearing"""
        with tempfile.TemporaryDirectory() as temp_dir:
            storage = SessionStorage(temp_dir)
            
            # Save and verify session exists
            storage.save_session({"test": "data"})
            assert storage.session_exists()
            
            # Clear session
            storage.clear_session()
            assert not storage.session_exists()
            assert storage.load_session() is None
    
    def test_corrupted_session_handling(self):
        """Test handling of corrupted session files"""
        with tempfile.TemporaryDirectory() as temp_dir:
            storage = SessionStorage(temp_dir)
            
            # Create corrupted session file
            with open(storage.session_file, 'w') as f:
                f.write("corrupted data")
            
            # Should return None and clean up
            result = storage.load_session()
            assert result is None
            assert not storage.session_exists()
