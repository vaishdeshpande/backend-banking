from fastapi import HTTPException, status

class AccountAlreadyExists(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail="Account already exists")

class AccountDoesNotExists(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail="Account with specified account number does not exist")

class InvalidAccountType(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid account type")

class InternalServerError(HTTPException):
    def __init__(self, message):
        super().__init__(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=message)

class InvalidDepositAmount(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST,
                         detail="Invalid deposit amount. Amount must be a positive numeric value.")

class InvalidWithdrawAmount(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST,
                         detail="Invalid withdrawal amount. Amount must be a positive numeric value.")

class KycRequired(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST,
                         detail="KYC is required for deposit amount greater than 50000")

class ExceededMonthlyDeposit(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST,
                         detail="Deposit amount exceeds the maximum monthly deposit limit for the account")

class ExceededMonthlyWithdrawlLimit(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST,
                         detail="You have exceeded monthly withdrawal transactions limit")

class InsufficientBalance(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST,
                         detail="Account does not have sufficient balance")

class MinBalance(HTTPException):
    def __init__(self, min_balance, account_type_name):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST,
                         detail=f"The system enforces a minimum balance requirement of {min_balance} rupees for {account_type_name} accounts and withdrawals beyond this minimum balance are not permitted.")
