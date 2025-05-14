from typing import Any

from pydantic import BaseModel


class CreateBankAccountResponse(BaseModel):
    success: bool = True
    error_text: str | None = None


class TransferResponse(BaseModel):
    success: bool = True
    error_text: str | None = None


class StatusResponse(BaseModel):
    status: str = "Processing"
    error_text: str | None = None


class ExchangeRateResponse(BaseModel):
    currencies: dict
    error_text: str | None = None
