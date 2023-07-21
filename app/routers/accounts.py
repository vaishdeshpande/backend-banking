# app/routers/accounts.py
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..controller.account_controller import AccountController
from ..repository.account_repository import AccountRepository
from ..models.models import AccountModel,AccountTypeDetailsMode
from ..config.database import get_db

router = APIRouter(
    prefix="/accounts",
    tags=['Accounts']
)

account_repo = AccountRepository()

account_controller = AccountController(account_repo)

@router.post("/create")
def create_account(account: AccountModel,db: Session = Depends(get_db)):
    
    account_controller.create_account(account,db)
    return {"message": "Account created successfully"}

@router.post("/addAccountType")
async def add_account_type(account_type: AccountTypeDetailsMode,db: Session = Depends(get_db)):
    
    await account_controller.add_account_type(account_type,db)
    return {"message": "Account Type added successfully"}











# session=db
    # zero_balance = AccountTypeDetails(
    #     id=AccountType.ZERO_BALANCE,
    #     account_type_name = "ZERO_BALANCE",
    #     max_withdrawals=4
    # )
    # session.add(zero_balance)

    # student = AccountTypeDetails(
    #     id=AccountType.STUDENT,
    #     account_type_name = "STUDENT",
    #     max_withdrawals=4,
    #     min_balance=1000,
    #     max_monthly_deposit=10000
    # )
    # session.add(student)

    # regular_saving = AccountTypeDetails(
    #     id=AccountType.REGULAR_SAVING,
    #     account_type_name = "REGULAR_SAVING",
    #     max_withdrawals=10,
    #     withdrawal_charge=5,
    # )
    # session.add(regular_saving)

    # session.commit()