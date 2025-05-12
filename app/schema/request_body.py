from typing import Any

from pydantic import BaseModel


class CreateBankAccountRequest(BaseModel):
    account_number: int
    holder_first_name: str
    holder_last_name: str
    balance: int = 0
    email: str = ''


class TransferRequest(BaseModel):
    account_number_receiver: int
    account_number_sender: int
    amount: int = 0


class StatusRequest(BaseModel):
    account_number: int


