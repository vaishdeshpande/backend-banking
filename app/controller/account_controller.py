# app/controller/account_controller.py
from datetime import datetime
from fastapi import FastAPI, HTTPException, APIRouter,Depends,status
from ..models.schemas import Account,AccountTypeDetails
from ..models.models import AccountTypeDetailsMode
from ..repository.account_repository import AccountRepository
from ..exceptions.exception_handler import InvalidAccountType,AccountAlreadyExists,InternalServerError
from sqlalchemy.orm import Session
from ..utils.logger import logger_class

@logger_class
class AccountController:
    def __init__(self, account_repo: AccountRepository):
        self.account_repo = account_repo

    async def create_account(self, accountObj,db: Session):
        try:
            # Creating account
            account_type_details = self.account_repo.get_account_type_details(accountObj.account_type_id,db)
            if not account_type_details:    
                raise InvalidAccountType()
            
            # Validation for account Already Exists 
            if self.account_repo.get_account(accountObj.account_number,db):
                raise AccountAlreadyExists()

            new_account = Account(
                account_number=accountObj.account_number,
                account_type_id=accountObj.account_type_id,
                account_type_details=account_type_details,
                balance = accountObj.balance,
                current_month_deposit = accountObj.balance,
                last_deposit_month = datetime.now().month,
                last_deposit_year = datetime.now().year
            )
            self.account_repo.add_account(new_account,db)
            self.account_repo.save_changes(db)
        
        except HTTPException as http_exc:
            raise http_exc

        except Exception as e:
            raise InternalServerError("An unexpected error occurred while creation of the account")

    async def add_account_type(self,new_account_type: AccountTypeDetailsMode,db: Session ):
        try:
            account_type = AccountTypeDetails( **new_account_type.dict())
            self.account_repo.add_account_type(account_type,db)
            self.account_repo.save_changes(db)
            return 
        except HTTPException as http_exc:
            raise http_exc

        except Exception as e:
            raise HTTPException("An unexpected error occurred while creation of new accountType")



