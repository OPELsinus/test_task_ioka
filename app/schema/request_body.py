from typing import Any

from pydantic import BaseModel, EmailStr


class TransferRequest(BaseModel):
    account_number_receiver: int
    account_number_sender: int
    amount: int = 0


class CreateUserAccount(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    login: str
    password: str


class LoginRequest(BaseModel):
    login: str
    password: str


class CreateBankAccountRequest(BaseModel):
    account_number: int
    balance: int = 0
    account_currency: str


class ExchangeRequest(BaseModel):
    account_sender: str
    account_receiver: str
    amount: float
