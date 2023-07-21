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
async def create_account(account: AccountModel,db: Session = Depends(get_db)):
    
    await account_controller.create_account(account,db)
    return {"message": "Account created successfully"}

@router.post("/addAccountType")
async def add_account_type(account_type: AccountTypeDetailsMode,db: Session = Depends(get_db)):
    
    await account_controller.add_account_type(account_type,db)
    return {"message": "Account Type added successfully"}











