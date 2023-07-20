import pytest
from datetime import datetime
from unittest.mock import MagicMock
from utils.logger import logger_class
from exceptions.exception_handler import KycRequired, ExceededMonthlyDeposit, AccountDoesNotExists, InvalidDepositAmount
from models.schemas import AccountTypeDetails, Account
from validators.deposit_validator import DepositValidator

@pytest.fixture
def deposit_validator(account_repo_mock, account_mock, account_type_details_mock):
    deposit_validator = DepositValidator()
    deposit_validator.account_repo = account_repo_mock
    account_repo_mock.get_account_type_details.return_value = account_type_details_mock
    return deposit_validator

@pytest.fixture
def account_mock():
    return Account(
        account_number="12345",
        balance=5000,
        kyc_flag=True,
        account_type_id=1,
        current_month_deposit=0,
        last_deposit_month=datetime.now().month,
        last_deposit_year=datetime.now().year,
    )

@pytest.fixture
def account_type_details_mock(account_repo_mock):
    account_type_details_mock = AccountTypeDetails(
        id=1,
        account_type_name="Regular Savings",
        max_monthly_deposit=50000,
        max_withdrawals=5,
        min_balance=1000,
        further_withdrawls_blocked=True,
        withdrawal_charge=50
    )
    account_repo_mock.get_account_type_details.return_value = account_type_details_mock
    return account_type_details_mock

@pytest.fixture
def account_repo_mock():
    return MagicMock()

# Rest of the test cases remain the same...


# def test_validate_max_deposit_valid(deposit_validator, account_mock, account_type_details_mock):
#     # Test when the deposit amount is less than the max monthly deposit
#     amount = 10000
#     assert deposit_validator.validate_max_deposit(account_mock, account_type_details_mock, amount) is True

# def test_validate_max_deposit_exceeded(deposit_validator, account_mock, account_type_details_mock):
#     # Test when the deposit amount exceeds the max monthly deposit
#     amount = 60000
#     with pytest.raises(ExceededMonthlyDeposit):
#         deposit_validator.validate_max_deposit(account_mock, account_type_details_mock, amount)

# def test_validate_deposit_request_valid(deposit_validator, account_mock):
#     # Test when the deposit request is valid
#     db_mock = MagicMock()
#     amount = 10000
#     assert deposit_validator.validate_deposit_request(account_mock, amount, db_mock) is True

def test_validate_deposit_request_invalid(deposit_validator, account_mock):
    # Test when the account is None
    db_mock = MagicMock()
    amount = 10000
    with pytest.raises(AccountDoesNotExists):
        deposit_validator.validate_deposit_request(None, amount, db_mock)

def test_validate_deposit_request_negative_amount(deposit_validator, account_mock):
    # Test when the deposit amount is negative
    db_mock = MagicMock()
    amount = -10000
    with pytest.raises(InvalidDepositAmount):
        deposit_validator.validate_deposit_request(account_mock, amount, db_mock)

def test_validate_deposit_request_kyc_required(deposit_validator, account_mock):
    # Test when the deposit amount exceeds the KYC limit
    db_mock = MagicMock()
    account_mock.kyc_flag = False
    amount = 60000
    with pytest.raises(KycRequired):
        deposit_validator.validate_deposit_request(account_mock, amount, db_mock)
