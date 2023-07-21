# tests/test_account_controller.py

import pytest
from fastapi import HTTPException, status
from app.controller.account_controller import AccountController
from app.models.schemas import AccountTypeDetails
from app.models.models import AccountModel
from app.repository.account_repository import AccountRepository
from unittest.mock import MagicMock

@pytest.fixture
def account_repo_mock():
    return MagicMock(spec=AccountRepository)


@pytest.fixture
def account_controller(account_repo_mock):
    return AccountController(account_repo_mock)


def test_create_account_success(account_controller, account_repo_mock):
    account_obj = AccountModel(account_number="12345", balance=1000.0, account_type_id=1)
    account_repo_mock.get_account_type_details.return_value = AccountTypeDetails(
        id=1,
        account_type_name="REGULAR_SAVING",
        max_monthly_deposit=50000,
        max_withdrawals=5,
        min_balance=1000,
        further_withdrawls_blocked=True,
        withdrawal_charge=50
    )
    account_repo_mock.get_account.return_value = None

    account_controller.create_account(account_obj, None)



def test_create_account_invalid_account_type(account_controller, account_repo_mock):
    account_obj = AccountModel(account_number="12345", balance=1000.0, account_type_id=10)
    account_repo_mock.get_account_type_details.return_value = None

    with pytest.raises(HTTPException) as context:
        account_controller.create_account(account_obj, None)

    assert context.value.status_code == status.HTTP_400_BAD_REQUEST
    assert context.value.detail == "Invalid account type"
    