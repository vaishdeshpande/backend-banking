# tests/test_transaction_controller.py

import pytest
from datetime import datetime
from unittest.mock import MagicMock
from app.models.schemas import AccountTypeDetails, Account
from app.models.models import TransactionHistoryModel
from app.controller.transaction_controller import TransactionController
from app.repository.account_repository import AccountRepository
from app.validators.deposit_validator import DepositValidator
from app.validators.withdrawl_validator import WithdrawlValidator


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

    # Create mocks for validators (DepositValidator and WithdrawlValidator)
    deposit_validator_mock = MagicMock(spec=DepositValidator)
    withdrawl_validator_mock = MagicMock(spec=WithdrawlValidator)

    # Create the TransactionController using the mocks
    transaction_controller = TransactionController()

    # Return the mock data and TransactionController as a dictionary
    return {
        'account_number': account_number,
        'amount': amount,
        'db_mock': db_mock,
        'account_mock': account_mock,
        'account_type_details_mock': account_type_details_mock,
        'account_repo_mock': account_repo_mock,
        'deposit_validator_mock': deposit_validator_mock,
        'withdrawl_validator_mock': withdrawl_validator_mock,
        'transaction_controller': transaction_controller,
    }

def test_deposit_success(mock_data):
    account_number = mock_data['account_number']
    amount = mock_data['amount']
    db_mock = mock_data['db_mock']
    account_mock = mock_data['account_mock']
    account_type_details_mock = mock_data['account_type_details_mock']
    transaction_controller = mock_data['transaction_controller']

    # Save the initial balance before the deposit
    initial_balance = account_mock.balance

    # Perform the deposit
    transaction_controller.deposit(account_number, amount, db_mock)

    # Check if the balance is updated correctly after the deposit
    assert account_mock.balance == initial_balance + amount


def test_withdraw_success(mock_data):
    account_number = mock_data['account_number']
    amount = mock_data['amount']
    db_mock = mock_data['db_mock']
    account_mock = mock_data['account_mock']
    account_type_details_mock = mock_data['account_type_details_mock']
    transaction_controller = mock_data['transaction_controller']

    # Save the initial balance before the deposit
    initial_balance = account_mock.balance

    # Perform the deposit
    transaction_controller.withdraw(account_number, amount, db_mock)

    # Check if the balance is updated correctly after the deposit
    assert account_mock.balance == initial_balance - amount


def test_get_transaction_history_account_exists(mock_data):
    # Extract the required data from the mock_data fixture
    account_number = mock_data['account_number']
    db_mock = mock_data['db_mock']
    account_mock = mock_data['account_mock']
    account_type_details_mock = mock_data['account_type_details_mock']
    transaction_controller = mock_data['transaction_controller']

    # Assume some dummy transaction data for testing
    dummy_transactions = [
        # List of Transaction objects or dictionaries with required fields
    ]

    # Set up the mock behavior for get_account and get_transactions_by_date_range_paginated
    mock_data['account_repo_mock'].get_account.return_value = account_mock
    mock_data['account_repo_mock'].get_transactions_by_date_range_paginated.return_value = (
        dummy_transactions, 20, 2  # transactions, total_transactions, total_pages
    )

    # Create a dummy TransactionHistoryModel object for the test
    transaction_history_req = TransactionHistoryModel(
        account_number=account_number,
        from_date=datetime(2023, 1, 1),
        to_date=datetime(2023, 2, 1),
        page=1
    )

    # Call the get_transaction_history function
    result = transaction_controller.get_transaction_history(transaction_history_req, db_mock)

    # Check the result to ensure it is as expected
    assert result["account_number"] == account_number
    assert result["total_transactions"] == 20
    assert result["current_page"] == 1
    assert result["total_pages"] == 2
    assert result["transactions"] == dummy_transactions
