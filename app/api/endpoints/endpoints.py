from fastapi import APIRouter
from starlette import status

from app.schema.request_body import CreateBankAccountRequest, TransferRequest
from app.schema.response_body import CreateBankAccountResponse, TransferResponse
from app.service.services import create_bank_account_response, create_transfer_response

router = APIRouter()


@router.get("/health")
async def test_api():
    return {"status_code": status.HTTP_200_OK}


@router.post("/create_bank_account")
# @try_execute_async
async def create_bank_account(request_body: CreateBankAccountRequest) -> CreateBankAccountResponse:
    response_data = CreateBankAccountResponse()

    return await create_bank_account_response(response_data=response_data, request_body=request_body)


@router.post("/create_transfer")
# @try_execute_async
async def create_bank_account(request_body: TransferRequest) -> TransferResponse:
    response_data = TransferResponse()

    return await create_transfer_response(response_data=response_data, request_body=request_body)
