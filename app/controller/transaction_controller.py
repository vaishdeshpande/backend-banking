# app/controller/transaction_controller.py
from ..models.schemas import Account ,AccountType,Transaction,TransactionType,AccountTypeDetails
from ..models.models import TransactionHistoryModel
from datetime import datetime
from fastapi import FastAPI, HTTPException, APIRouter,Depends,status
from ..exceptions.exception_handler import InternalServerError,InvalidDepositAmount,AccountDoesNotExists
from ..utils.logger import logger_class
import logging
from ..repository.account_repository import AccountRepository
from ..validators.deposit_validator import DepositValidator
from ..validators.withdrawl_validator import WithdrawlValidator
@logger_class
class TransactionController:
    def __init__(self):
        self.account_repo = AccountRepository()
        self.deposit_validator = DepositValidator()
        self.withdrawl_validator = WithdrawlValidator()

    def deposit(self, account_number: str, amount: int,db):
        try:
            logging.info(f'validate the deposit request')
            account = self.account_repo.get_account(account_number,db)
            #validate the deposit request
            self.deposit_validator.validate_deposit_request(account,amount,db)
            
            logging.info(f'# Perform the deposit')
            # Perform the deposit
            account.balance += amount

            #Set the latest month and year in the account 
            account.last_deposit_month = datetime.now().month
            account.last_deposit_year = datetime.now().year
            logging.info(f'Set current month deposit')
            
            #Set current month deposit
            if datetime.now().month == account.last_deposit_month and datetime.now().year == account.last_deposit_year:
                account.current_month_deposit += amount
            else:
                account.current_month_deposit = amount

            logging.info(f'Create transaction record')
            # Create transaction record
            transaction = Transaction(
                account_number=account.account_number,
                type=TransactionType.DEPOSIT,
                amount=amount,
                timestamp=datetime.utcnow()
            )
            account.transactions.append(transaction)

            balance = account.balance
            logging.info(f'Updating the database with changes')
            # Updating the database with changes
            self.account_repo.save_changes(db)
            return balance
        except HTTPException as httpexc:
            raise httpexc
        except ValueError:
            # Invalid deposit amount (negative amount or non-numeric)
            raise  InvalidDepositAmount()
        except Exception as e:
            logging.error(e)
            raise InternalServerError("An unexpected error occurred while processing the deposit")



    def withdraw(self, account_number: str, amount: int,db):
        try:
            account = self.account_repo.get_account(account_number,db)
            # Check withdrawal rules and account_type_details
            account_type_details =  self.withdrawl_validator.validate_withdraw_request(account,amount,db)

            # Create transaction record
            transaction = Transaction(
                account_number=account.account_number,
                type=TransactionType.WITHDRAWAL,
                amount=amount,
                timestamp=datetime.utcnow(),
                
            )

            current_month = datetime.now().month
            current_year = datetime.now().year
            if current_month == account.last_withdraw_month and current_year == account.last_withdraw_year:
                account.current_month_withdraw_count +=1
                if account.current_month_withdraw_count > account.account_type_details.max_withdrawals and account_type_details.withdrawal_charge!=None:
                    account.balance -= amount + account.account_type_details.withdrawal_charge
                    transaction.transaction_charge= account_type_details.withdrawal_charge 
                else:
                    account.balance -= amount
            else:
                account.current_month_withdraw_count =1
                account.last_withdraw_month = current_month
                account.last_withdraw_year = current_year

            account.transactions.append(transaction)
            balance = account.balance
            self.account_repo.save_changes(db)
            return balance
        except HTTPException as httpexc:
            raise httpexc
        
        except Exception as e:
            logging.error(e)
            raise InternalServerError("An unexpected error occurred while processing the withdraw")

    def get_transaction_history(self, transaction_history_req: TransactionHistoryModel, db, page_size: int = 10):
        
        account =  self.account_repo.get_account(transaction_history_req.account_number,db)
        if account is None:
                raise AccountDoesNotExists()
        
        transactions, total_transactions,total_pages= self.account_repo.get_transactions_by_date_range_paginated(
            transaction_history_req.account_number, transaction_history_req.from_date, transaction_history_req.to_date,db, transaction_history_req.page, page_size
        )

        return {
            "account_number": transaction_history_req.account_number,
            "total_transactions": total_transactions,
            "current_page": transaction_history_req.page,
            "total_pages" : total_pages,
            "transactions": transactions,
        }
    