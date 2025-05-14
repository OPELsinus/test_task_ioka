from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette import status
from starlette.status import HTTP_303_SEE_OTHER

from app.error_handler.error_handler import try_execute_async
from app.schema.request_body import (
    CreateBankAccountRequest,
    TransferRequest,
    CreateUserAccount,
    LoginRequest,
    ExchangeRequest,
)
from app.schema.response_body import (
    CreateBankAccountResponse,
    TransferResponse,
    ExchangeRateResponse,
)
from app.service.services import (
    create_bank_account_response,
    create_transfer_response,
    get_exchange_rates,
    create_exchange_response,
)
from app.settings.config import config
from app.settings.database import User, db_session
from app.security.security import (
    get_password_hash,
    verify_password,
    create_access_token,
    get_current_user,
    ACCESS_TOKEN_EXPIRE_MINUTES,
)

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


# API Endpoints (keep your existing ones)
@router.get("/health")
async def test_api():
    return {"status_code": status.HTTP_200_OK}


@router.post("/api/create_transfer")
async def api_create_transfer(request_body: TransferRequest) -> TransferResponse:
    response_data = TransferResponse()
    return await create_transfer_response(
        response_data=response_data, request_body=request_body
    )


@router.post("/api/register")
async def api_register(user_data: CreateUserAccount):
    with db_session() as session:
        if session.query(User).filter(User.email == user_data.email).first():
            raise HTTPException(status_code=400, detail="Email already registered")
        if session.query(User).filter(User.login == user_data.login).first():
            raise HTTPException(status_code=400, detail="Login already taken")

        hashed_password = get_password_hash(user_data.password)
        new_user = User(
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            email=user_data.email,
            login=user_data.login,
            password_hash=hashed_password,
        )
        session.add(new_user)
        session.commit()
    return {"message": "User registered successfully"}


@router.post("/api/login")
async def api_login(login_data: LoginRequest):
    with db_session() as session:
        user = session.query(User).filter(User.login == login_data.login).first()
        if not user or not verify_password(login_data.password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect login or password",
            )
        access_token = create_access_token(data={"sub": user.login})
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/api/create_bank_account")
async def api_create_bank_account(
    request_body: CreateBankAccountRequest,
    current_user: User = Depends(get_current_user),
) -> CreateBankAccountResponse:
    response_data = CreateBankAccountResponse()
    return await create_bank_account_response(response_data, request_body, current_user)


@router.get("/api/exchange_rates")
async def api_get_exchange_rates() -> ExchangeRateResponse:
    return await get_exchange_rates()


@router.post("/api/exchange")
async def api_exchange(
    request_body: ExchangeRequest, current_user: User = Depends(get_current_user)
) -> TransferResponse:
    response_data = TransferResponse()
    return await create_exchange_response(response_data, request_body, current_user)


@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        "index.html", {"request": request, "loc": config.LOCALIZATION}
    )


@router.post("/register", response_class=RedirectResponse)
async def form_register(
    request: Request,
    first_name: str = Form(...),
    last_name: str = Form(...),
    email: str = Form(...),
    login: str = Form(...),
    password: str = Form(...),
):
    user_data = CreateUserAccount(
        first_name=first_name,
        last_name=last_name,
        email=email,
        login=login,
        password=password,
    )
    await api_register(user_data)
    return RedirectResponse(url="/login", status_code=HTTP_303_SEE_OTHER)


@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse(
        "login.html", {"request": request, "loc": config.LOCALIZATION}
    )


@router.post("/login", response_class=RedirectResponse)
async def form_login(
    request: Request, login: str = Form(...), password: str = Form(...)
):
    login_data = LoginRequest(login=login, password=password)
    response = await api_login(login_data)

    redirect = RedirectResponse(url="/main_page", status_code=HTTP_303_SEE_OTHER)
    redirect.set_cookie(
        key="access_token",
        value=f"Bearer {response['access_token']}",
        httponly=True,
        secure=False,
        samesite="lax",
    )
    return redirect


@router.get("/main_page", response_class=HTMLResponse)
async def dashboard(request: Request, current_user: User = Depends(get_current_user)):
    exchange_rates = await api_get_exchange_rates()
    return templates.TemplateResponse(
        "main_page.html",
        {
            "request": request,
            "user": current_user,
            "currencies": exchange_rates.currencies,
            "loc": config.LOCALIZATION,
        },
    )


@router.post("/create_bank_account", response_class=RedirectResponse)
async def form_create_bank_account(
    request: Request,
    account_number: int = Form(...),
    balance: int = Form(0),
    account_currency: str = Form(1),
    current_user: User = Depends(get_current_user),
):
    request_body = CreateBankAccountRequest(
        account_number=account_number,
        balance=balance,
        account_currency=account_currency,
    )
    response = await api_create_bank_account(request_body, current_user)
    if not response.success:
        error_msg = response.error_text
        return templates.TemplateResponse(
            "main_page.html",
            {
                "request": request,
                "user": current_user,
                "currencies": await get_exchange_rates(),
                "loc": config.LOCALIZATION,
                "error": error_msg,
            },
        )

    return RedirectResponse(
        url="/main_page?success=Account+created", status_code=HTTP_303_SEE_OTHER
    )


@router.post("/exchange", response_class=RedirectResponse)
async def form_exchange(
    request: Request,
    account_sender: str = Form(...),
    account_receiver: str = Form(...),
    amount: float = Form(...),
    current_user: User = Depends(get_current_user),
):
    request_body = ExchangeRequest(
        account_sender=account_sender, account_receiver=account_receiver, amount=amount
    )
    await api_exchange(request_body, current_user)
    return RedirectResponse(url="/main_page", status_code=HTTP_303_SEE_OTHER)


@router.post("/logout", response_class=RedirectResponse)
async def logout():
    redirect = RedirectResponse(url="/", status_code=HTTP_303_SEE_OTHER)
    redirect.delete_cookie("access_token")
    return redirect
