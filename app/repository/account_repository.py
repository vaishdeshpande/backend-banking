# app/repository/account_repository.py
from fastapi import FastAPI, HTTPException, APIRouter,Depends
from ..config.database import get_db
from ..models.schemas import Account,AccountTypeDetails,Transaction
from sqlalchemy.orm import Session 
from sqlalchemy import func
from ..utils.logger import logger_class
import logging
@logger_class
class AccountRepository:

    def get_account(self, account_number: str,db: Session ):
        logging.info(f'get_account')
        account = db.query(Account).filter_by(account_number=account_number).first()      

        if not account:
            return None

        return account
    
    def get_account_type_details(self,account_type_id:int,db:Session):
        logging.info(f'get_account_type_details')
        account_type_details = db.query(AccountTypeDetails).filter_by(id=account_type_id).first()
        
        if not account_type_details:
            return None
        return account_type_details
    
    def add_account(self, account: Account, db: Session):
        db.add(account)

    def add_account_type(self, account_type_details: AccountTypeDetails, db: Session):
        db.add(account_type_details)
    
    def get_transactions_by_date_range_paginated(self, account_number: str, from_date: str, to_date: str, db: Session,page:int ,page_size:int = 10):
        logging.info(f'get_transactions_by_date_range_paginated')
        # Query to count the total number of transactions within the date range
        count_query = db.query(func.count(Transaction.id)).filter(Transaction.account_number ==  account_number)

        # Query to fetch the paginated transactions within the date range
        query = db.query(Transaction).filter(Transaction.account_number == account_number)

        if from_date:
            count_query = count_query.filter(Transaction.timestamp >= from_date)
            query = query.filter(Transaction.timestamp >= from_date)

        if to_date:
            count_query = count_query.filter(Transaction.timestamp <= to_date)
            query = query.filter(Transaction.timestamp <= to_date)

        total_transactions = count_query.scalar()

        # Calculate the total number of pages
        total_pages = (total_transactions + page_size - 1) // page_size

        # Handle edge cases for page parameter
        if page < 1 or page > total_pages:
            logging.error(f'Page:{page},Total_pages:{total_pages}')
            raise HTTPException(status_code=400, detail="Invalid page number.")

        # Calculate the offset to fetch the correct page of records
        offset = (page - 1) * page_size

        # Limit the number of records and fetch the transactions
        transactions = query.order_by(Transaction.timestamp).limit(page_size).all()

        return transactions, total_transactions,total_pages

    def save_changes(self,db: Session ):
        logging.info(f'get_transactions_by_date_range_paginated')
        db.commit()
        db.close()
    