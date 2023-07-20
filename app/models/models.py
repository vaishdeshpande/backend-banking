from pydantic import BaseModel,Field
from datetime import datetime,timedelta

class AccountModel(BaseModel):
    account_number :str
    balance : float
    kyc_flag : bool = False
    account_type_id : int

class TransactionModel(BaseModel):
    account_number :str
    amount : float

class TransactionHistoryModel(BaseModel):
    account_number :str
    from_date: datetime = Field(default=datetime.today().replace(day=1))
    to_date: datetime = Field(default=datetime.today())
    page:int=1
    


    