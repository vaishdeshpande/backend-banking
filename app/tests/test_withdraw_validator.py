import pytest
from datetime import datetime
from unittest.mock import MagicMock
from utils.logger import logger_class
from exceptions.exception_handler import (
    ExceededMonthlyWithdrawlLimit, MinBalance, InsufficientBalance, AccountDoesNotExists, InvalidWithdrawAmount
)
from models.schemas import AccountTypeDetails, Account
from validators.withdrawl_validator import WithdrawlValidator
from repository.account_repository import AccountRepository

@pytest.fixture
def mock_data():
    account_number = "12345"
    amount = 1000
    db_mock = MagicMock()

    # Create a mock for the AccountTypeDetails
    account_type_details_mock = AccountTypeDetails(
        id=1,
        account_type_name="Regular Savings",
        max_monthly_deposit=50000,
        max_withdrawals=5,
        min_balance=1000,
        further_withdrawls_blocked=True,
        withdrawal_charge=50
    )

    # Create a mock for the Account object
    account_mock = MagicMock(spec=Account)
    account_mock.account_number = account_number
    account_mock.balance = 5000  # Set the initial balance here
    account_mock.kyc_flag = True
    account_mock.account_type_id = 1
    account_mock.current_month_deposit = 0  # Set initial deposit for the month
    account_mock.last_deposit_month = datetime.now().month
    account_mock.last_deposit_year = datetime.now().year
    account_mock.current_month_withdraw_count = 0
    account_mock.last_withdraw_month = datetime.now().month
    account_mock.last_withdraw_year = datetime.now().year
    account_mock.account_type_details = account_type_details_mock

    # Create a mock for the AccountRepository
    account_repo_mock = MagicMock(spec=AccountRepository)
    account_repo_mock.get_account.return_value = account_mock
    account_repo_mock.get_account_type_details.return_value = account_type_details_mock

    # Create an instance of WithdrawlValidator using the account_repo_mock
    withdrawl_validator = WithdrawlValidator()
    withdrawl_validator.account_repo = account_repo_mock

    # Return the mock data and WithdrawlValidator instance as a dictionary
    return {
        'account_number': account_number,
        'amount': amount,
        'db_mock': db_mock,
        'account_mock': account_mock,
        'account_type_details_mock': account_type_details_mock,
        'withdrawl_validator': withdrawl_validator,
    }


def test_validate_withdraw_request_valid(mock_data):
    # Test when the withdraw request is valid
    account_mock = mock_data['account_mock']
    amount = 1000
    db_mock = mock_data['db_mock']
    withdrawl_validator = mock_data['withdrawl_validator']

    result = withdrawl_validator.validate_withdraw_request(account_mock, amount, db_mock)
    assert result == mock_data['account_type_details_mock']

def test_validate_withdraw_request_invalid_account(mock_data):
    # Test when the account does not exist
    db_mock = mock_data['db_mock']
    withdrawl_validator = mock_data['withdrawl_validator']

    with pytest.raises(AccountDoesNotExists):
        withdrawl_validator.validate_withdraw_request(None, 1000, db_mock)

def test_validate_withdraw_request_invalid_amount(mock_data):
    # Test when the withdrawal amount is negative
    account_mock = mock_data['account_mock']
    db_mock = mock_data['db_mock']
    withdrawl_validator = mock_data['withdrawl_validator']

    with pytest.raises(InvalidWithdrawAmount):
        withdrawl_validator.validate_withdraw_request(account_mock, -500, db_mock)

def test_validate_withdraw_request_exceeded_monthly_limit(mock_data):
    # Test when the monthly withdrawal limit is exceeded
    account_mock = mock_data['account_mock']
    account_type_details_mock = mock_data['account_type_details_mock']
    account_mock.current_month_withdraw_count = 5  # Set the current_month_withdraw_count to the max limit
    db_mock = mock_data['db_mock']
    withdrawl_validator = mock_data['withdrawl_validator']

    with pytest.raises(ExceededMonthlyWithdrawlLimit):
        withdrawl_validator.validate_withdraw_request(account_mock, 1000, db_mock)

def test_validate_withdraw_request_min_balance(mock_data):
    # Test when the balance after withdrawal is less than the minimum balance requirement
    account_mock = mock_data['account_mock']
    account_type_details_mock = mock_data['account_type_details_mock']
    account_mock.balance = 3000  # Set the balance to be less than the minimum balance
    db_mock = mock_data['db_mock']
    withdrawl_validator = mock_data['withdrawl_validator']

    with pytest.raises(MinBalance):
        withdrawl_validator.validate_withdraw_request(account_mock, 2100, db_mock)

