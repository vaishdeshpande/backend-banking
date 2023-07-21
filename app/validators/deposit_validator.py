# app/validators/deposit_validator.py
# Responsible for validating deposit requests and enforcing deposit rules. 
# It includes methods to validate deposit requests, maximum monthly deposits, and KYC requirements.
from datetime import datetime
from fastapi import FastAPI, HTTPException,status
from ..exceptions.exception_handler import KycRequired,ExceededMonthlyDeposit, AccountDoesNotExists,InvalidDepositAmount
from ..utils.logger import logger_class
from ..repository.account_repository import AccountRepository
@logger_class
class DepositValidator:

    def __init__(self) -> None:
        self.account_repo = AccountRepository()
   
    def validate_deposit_request(self,account,amount,db):
        if account is None:
            raise AccountDoesNotExists()
        if amount < 0:
            raise InvalidDepositAmount()
        account_type_details = self.account_repo.get_account_type_details(account.account_type_id,db)
        self.validate_max_deposit(account,account_type_details,amount)
        
     
    def validate_max_deposit(self,account,account_type_details,amount):
        current_month = datetime.now().month
        current_year = datetime.now().year
        # Check deposit rules
        if amount > 50000 and not account.kyc_flag:
            raise KycRequired()
        if account_type_details.max_monthly_deposit != None and account_type_details.max_monthly_deposit != 0:
            if current_month == account.last_deposit_month and current_year == account.last_deposit_year and account.current_month_deposit + amount > account.account_type_details.max_monthly_deposit:
                raise ExceededMonthlyDeposit()
        
        return True