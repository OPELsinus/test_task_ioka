from app.schema.request_body import (
    CreateBankAccountRequest,
    TransferRequest,
    ExchangeRequest,
)
from app.schema.response_body import (
    CreateBankAccountResponse,
    TransferResponse,
    ExchangeRateResponse,
)
from app.settings.database import (
    insert_new_account_into_db,
    insert_new_transfer_into_db,
    db_session,
    ExchangeRate,
    BankAccount,
    get_exchange_rate,
    get_currency,
)


async def create_bank_account_response(
    response_data: CreateBankAccountResponse,
    request_body: CreateBankAccountRequest,
    user,
):
    insert_new_account_into_db(request_body, user)
    return response_data


async def create_transfer_response(
    response_data: TransferResponse, request_body: TransferRequest
):
    insert_new_transfer_into_db(request_body)
    return response_data


async def get_exchange_rates() -> ExchangeRateResponse:
    with db_session() as session:
        rates = session.query(ExchangeRate).all()
        currencies = {rate.currency: rate.rate for rate in rates}
        return ExchangeRateResponse(currencies=currencies)


async def create_exchange_response(
    response_data: TransferResponse, request_body: ExchangeRequest, current_user
):
    with db_session() as session:
        sender_currency = get_currency(request_body.account_sender)
        receiver_currency = get_currency(request_body.account_receiver)

        from_rate = float(get_exchange_rate(sender_currency))
        to_rate = float(get_exchange_rate(receiver_currency))

        if not from_rate or not to_rate:
            response_data.success = False
            response_data.error_text = "Invalid currency"
            return response_data

        converted_amount = (request_body.amount / from_rate) * to_rate

        from_account = (
            session.query(BankAccount)
            .filter(
                BankAccount.user_id == current_user.id,
                BankAccount.account_number == request_body.account_sender,
            )
            .first()
        )

        to_account = (
            session.query(BankAccount)
            .filter(BankAccount.account_number == request_body.account_receiver)
            .first()
        )

        if not from_account or from_account.balance < request_body.amount:
            response_data.success = False
            response_data.error_text = "Insufficient funds or account not found"
            return response_data

        if not to_account:
            response_data.success = False
            response_data.error_text = (
                f"No account found for {request_body.account_receiver}"
            )
            return response_data

        from_account.balance = float(from_account.balance) - request_body.amount
        to_account.balance = float(to_account.balance) + converted_amount * 0.97

        session.commit()

    return response_data
