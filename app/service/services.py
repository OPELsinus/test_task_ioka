from app.schema.request_body import CreateBankAccountRequest, TransferRequest
from app.schema.response_body import CreateBankAccountResponse, TransferResponse
from app.settings.database import insert_new_account_into_db, insert_new_transfer_into_db


async def create_bank_account_response(response_data: CreateBankAccountResponse, request_body: CreateBankAccountRequest):
    print(request_body)
    insert_new_account_into_db(request_body)
    return response_data


async def create_transfer_response(response_data: TransferResponse, request_body: TransferRequest):
    print(request_body)
    insert_new_transfer_into_db(request_body)
    return response_data
