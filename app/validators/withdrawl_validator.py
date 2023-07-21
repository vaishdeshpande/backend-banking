# app/validators/withdrawl_validator.py
from datetime import datetime
from fastapi import FastAPI, HTTPException,status
from ..exceptions.exception_handler import ExceededMonthlyWithdrawlLimit,MinBalance,InsufficientBalance,AccountDoesNotExists,InvalidWithdrawAmount
from ..utils.logger import logger_class

@logger_class
class WithdrawlValidator:
    
    def validate_withdraw_request(self,account,amount,db):
        if account is None:
            raise AccountDoesNotExists()
        if amount < 0 or amount > account.balance:
            raise InvalidWithdrawAmount()
        account_type_details = self.account_repo.get_account_type_details(account.account_type_id,db)
        self.validate_max_withdrawl_limit(account,account_type_details,amount)
        self.validate_min_balance(account,account_type_details,amount)
        return account_type_details
    
    def validate_max_withdrawl_limit(self,account,account_type_details,amount):   
        
        if account_type_details.max_withdrawals is not None :
            if account.current_month_withdraw_count >= account_type_details.max_withdrawals and account_type_details.further_withdrawls_blocked==True:
                raise ExceededMonthlyWithdrawlLimit()
        
        return True
    
    def validate_min_balance(self,account,account_type_details,amount):

        min_balance = account_type_details.min_balance
        if min_balance is not None:
            if (account.balance - amount) < min_balance  :
                raise MinBalance(min_balance,account_type_details.account_type_name)
        
            elif amount > account.balance:
                raise InsufficientBalance()
        
        return True
    
    def validate_min_avg_balance(self,account,account_type_details,amount):
        pass
        # current_month = datetime.now().month
        # current_year = datetime.now().year
        # # Check deposit rules
        # if amount > 50000 and not account.kyc_flag:
        #     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
        #                     detail=f"KYC is required for deposit amount greater than 50000")
        # if account_type_details.max_monthly_deposit != None:
        #     if current_month == account.last_deposit_month and current_year == account.last_deposit_year and account.current_month_deposit + amount > account.account_type_details.max_monthly_deposit:
        #         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
        #                     detail=f"Deposit amount exceeds the maximum monthly deposit limit for the account")
        
        # return True