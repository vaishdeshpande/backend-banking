# app/validators/withdrawl_validator.py
"""
responsible for validating withdrawal requests and enforcing withdrawal rules.
 It includes methods to validate withdrawal requests,
 maximum withdrawals in a month, minimum balance requirements, and minimum average balance 
"""
from datetime import datetime
from fastapi import FastAPI, HTTPException,status
from ..exceptions.exception_handler import MinimumAverageBalance,ExceededMonthlyWithdrawlLimit,MinBalance,InsufficientBalance,AccountDoesNotExists,InvalidWithdrawAmount
from ..utils.logger import logger_class
from ..repository.account_repository import AccountRepository
from sqlalchemy.sql import func
from ..models.schemas import Account,Transaction
@logger_class
class WithdrawlValidator:

    def __init__(self) -> None:
        self.account_repo = AccountRepository()
    
    def validate_withdraw_request(self,account,amount,db):
        if account is None:
            raise AccountDoesNotExists()
        if amount < 0 or amount > account.balance:
            raise InvalidWithdrawAmount()
        account_type_details = self.account_repo.get_account_type_details(account.account_type_id,db)
        self.validate_max_withdrawl_limit(account,account_type_details,amount)
        self.validate_min_balance(account,account_type_details,amount)
        self.validate_min_avg_balance(account,account_type_details,amount,db)
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
    
    def validate_min_avg_balance(self,account,account_type_details,amount,db):
        if account_type_details.monthly_avg_balance is not None and account_type_details.monthly_avg_balance!=0:
            first_day_of_month = datetime.today().replace(day=1)

            balance_sum_query = db.query(func.sum(Account.balance)).filter(
                Account.account_number == account.account_number,
                Transaction.timestamp >= first_day_of_month
            )

            total_balance = balance_sum_query.scalar() - amount

            days_passed_in_month = (datetime.today() - first_day_of_month).days + 1

            
            avg_balance = total_balance / days_passed_in_month

            if avg_balance < account_type_details.monthly_avg_balance:
                raise MinimumAverageBalance()
        return True