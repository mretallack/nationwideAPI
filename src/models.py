"""Data models for accounts and balances"""

from dataclasses import dataclass
from decimal import Decimal
from datetime import datetime
from typing import Optional, List
import json

@dataclass
class Account:
    """Represents a Nationwide account"""
    account_id: str
    account_name: str
    account_type: str
    sort_code: str
    account_number: str
    
    def __post_init__(self):
        """Validate account data"""
        if not self.account_id:
            raise ValueError("Account ID is required")
        if not self.account_name:
            raise ValueError("Account name is required")
    
    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            'account_id': self.account_id,
            'account_name': self.account_name,
            'account_type': self.account_type,
            'sort_code': self.sort_code,
            'account_number': self.account_number
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Account':
        """Create from dictionary"""
        return cls(**data)

@dataclass
class Balance:
    """Represents account balance information"""
    account_id: str
    current_balance: Decimal
    available_balance: Decimal
    currency: str = "GBP"
    last_updated: Optional[datetime] = None
    
    def __post_init__(self):
        """Validate balance data"""
        if not self.account_id:
            raise ValueError("Account ID is required")
        if self.last_updated is None:
            self.last_updated = datetime.now()
    
    def format_currency(self, amount: Decimal) -> str:
        """Format amount as currency"""
        return f"£{amount:,.2f}"
    
    def current_balance_formatted(self) -> str:
        """Get formatted current balance"""
        return self.format_currency(self.current_balance)
    
    def available_balance_formatted(self) -> str:
        """Get formatted available balance"""
        return self.format_currency(self.available_balance)
    
    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            'account_id': self.account_id,
            'current_balance': str(self.current_balance),
            'available_balance': str(self.available_balance),
            'currency': self.currency,
            'last_updated': self.last_updated.isoformat() if self.last_updated else None
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Balance':
        """Create from dictionary"""
        return cls(
            account_id=data['account_id'],
            current_balance=Decimal(data['current_balance']),
            available_balance=Decimal(data['available_balance']),
            currency=data.get('currency', 'GBP'),
            last_updated=datetime.fromisoformat(data['last_updated']) if data.get('last_updated') else None
        )

@dataclass
class AccountSummary:
    """Combined account and balance information"""
    account: Account
    balance: Balance
    
    def __post_init__(self):
        """Validate that account and balance match"""
        if self.account.account_id != self.balance.account_id:
            raise ValueError("Account ID mismatch between account and balance")
    
    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            'account': self.account.to_dict(),
            'balance': self.balance.to_dict()
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'AccountSummary':
        """Create from dictionary"""
        return cls(
            account=Account.from_dict(data['account']),
            balance=Balance.from_dict(data['balance'])
        )

class AccountList:
    """Collection of account summaries"""
    
    def __init__(self, accounts: List[AccountSummary] = None):
        self.accounts = accounts or []
    
    def add_account(self, account_summary: AccountSummary):
        """Add an account summary"""
        self.accounts.append(account_summary)
    
    def get_account(self, account_id: str) -> Optional[AccountSummary]:
        """Get account by ID"""
        for account in self.accounts:
            if account.account.account_id == account_id:
                return account
        return None
    
    def total_balance(self) -> Decimal:
        """Calculate total current balance across all accounts"""
        return sum(account.balance.current_balance for account in self.accounts)
    
    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            'accounts': [account.to_dict() for account in self.accounts],
            'total_accounts': len(self.accounts),
            'total_balance': str(self.total_balance())
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'AccountList':
        """Create from dictionary"""
        accounts = [AccountSummary.from_dict(acc_data) for acc_data in data['accounts']]
        return cls(accounts)
    
    def to_json(self) -> str:
        """Convert to JSON string"""
        return json.dumps(self.to_dict(), indent=2)
    
    @classmethod
    def from_json(cls, json_str: str) -> 'AccountList':
        """Create from JSON string"""
        data = json.loads(json_str)
        return cls.from_dict(data)
