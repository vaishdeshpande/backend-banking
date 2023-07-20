from sqlalchemy import Column, Integer, String, Boolean, ForeignKey,DateTime,Float ,Enum as EnumColumn
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from datetime import datetime
from ..config.database import Base
from enum import Enum

class TransactionType(str, Enum):
    DEPOSIT = "deposit"
    WITHDRAWAL = "withdrawal"

class AccountType(int, Enum):
    ZERO_BALANCE = 1
    STUDENT = 2
    REGULAR_SAVING = 3

class Account(Base):
    __tablename__ = "accounts"

    account_number = Column(String, primary_key=True)
    balance = Column(Float, default=0)
    kyc_flag = Column(Boolean, default=False)
    transactions= relationship("Transaction", back_populates="account")
    account_type_id = Column(Integer, ForeignKey("account_type_details.id"))
    account_type_details = relationship("AccountTypeDetails")
    current_month_deposit = Column(Float, default=0)
    last_deposit_month = Column(Integer)
    last_deposit_year = Column(Integer)
    current_month_withdraw_count = Column(Integer, default=0)
    last_withdraw_month = Column(Integer)
    last_withdraw_year = Column(Integer)


class AccountTypeDetails(Base):
    __tablename__ = "account_type_details"

    id = Column(Integer, primary_key=True)
    account_type_name = Column(String)
    max_monthly_deposit = Column(Integer,default=None)
    max_withdrawals = Column(Integer,default=None)
    min_balance = Column(Integer,default=None)
    further_withdrawls_blocked = Column(Boolean,default=True)
    withdrawal_charge = Column(Integer,default=None)
    


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    account_number = Column(String, ForeignKey("accounts.account_number"))
    type = Column(String)
    amount = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)
    account = relationship("Account", back_populates="transactions")
    transaction_charge = Column(Float,default=None)

