# app/routers/transactions.py
from fastapi import  Depends, APIRouter
from sqlalchemy.orm import Session
from ..controller.transaction_controller import TransactionController
from ..models.models import TransactionModel,TransactionHistoryModel
from ..repository.account_repository import AccountRepository
from ..config.database import get_db
from ..validators.deposit_validator import DepositValidator
from ..validators.withdrawl_validator import WithdrawlValidator

router = APIRouter(
    prefix="/transaction",
    tags=['Accounts']
)

transaction_controller = TransactionController()

@router.put("/deposit")
def deposit(deposit: TransactionModel,db: Session = Depends(get_db)):
    balance =transaction_controller.deposit(deposit.account_number, deposit.amount,db)
    return {"message": "Deposit successful","account_balance":balance}


@router.put("/withdraw")
def withdraw(withdraw:TransactionModel,db: Session = Depends(get_db)):
    balance = transaction_controller.withdraw(withdraw.account_number, withdraw.amount,db)
    return {"message": "Withdrawal successful","account_balance":balance}


@router.post("/history")
def get_transaction_history(transaction_history_request:TransactionHistoryModel,db: Session = Depends(get_db)):
    transaction_history =  transaction_controller.get_transaction_history(transaction_history_request,db)
    return transaction_history