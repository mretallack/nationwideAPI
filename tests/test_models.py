"""Test data models"""

import pytest
from decimal import Decimal
from datetime import datetime
from src.models import Account, Balance, AccountSummary, AccountList

class TestAccount:
    def test_account_creation(self):
        """Test basic account creation"""
        account = Account(
            account_id="12345",
            account_name="Current Account",
            account_type="current",
            sort_code="12-34-56",
            account_number="12345678"
        )
        assert account.account_id == "12345"
        assert account.account_name == "Current Account"
    
    def test_account_validation(self):
        """Test account validation"""
        with pytest.raises(ValueError):
            Account("", "Test", "current", "12-34-56", "12345678")
    
    def test_account_serialization(self):
        """Test account to/from dict"""
        account = Account("123", "Test", "current", "12-34-56", "12345678")
        data = account.to_dict()
        account2 = Account.from_dict(data)
        assert account.account_id == account2.account_id

class TestBalance:
    def test_balance_creation(self):
        """Test basic balance creation"""
        balance = Balance(
            account_id="12345",
            current_balance=Decimal("1000.50"),
            available_balance=Decimal("950.00")
        )
        assert balance.current_balance == Decimal("1000.50")
        assert balance.currency == "GBP"
    
    def test_balance_formatting(self):
        """Test currency formatting"""
        balance = Balance("123", Decimal("1234.56"), Decimal("1000.00"))
        assert balance.current_balance_formatted() == "£1,234.56"
    
    def test_balance_serialization(self):
        """Test balance to/from dict"""
        balance = Balance("123", Decimal("100.00"), Decimal("90.00"))
        data = balance.to_dict()
        balance2 = Balance.from_dict(data)
        assert balance.current_balance == balance2.current_balance

class TestAccountList:
    def test_account_list_operations(self):
        """Test account list operations"""
        account = Account("123", "Test", "current", "12-34-56", "12345678")
        balance = Balance("123", Decimal("100.00"), Decimal("90.00"))
        summary = AccountSummary(account, balance)
        
        account_list = AccountList()
        account_list.add_account(summary)
        
        assert len(account_list.accounts) == 1
        assert account_list.total_balance() == Decimal("100.00")
        
        found = account_list.get_account("123")
        assert found is not None
        assert found.account.account_name == "Test"
