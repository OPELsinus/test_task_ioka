from contextlib import contextmanager
from decimal import Decimal

from app.schema.request_body import CreateBankAccountRequest, TransferRequest
from app.settings.config import config
from sqlalchemy import ForeignKey, Integer, Numeric, String, create_engine
from sqlalchemy.orm import (
    Mapped,
    declarative_base,
    mapped_column,
    sessionmaker,
    relationship,
)

Base = declarative_base()


@contextmanager
def db_session():
    """
    Context manager to handle database connection and session lifecycle.
    """
    SQLALCHEMY_DATABASE_URL = (
        f"postgresql://{config.DATABASE_USER}:{config.DATABASE_PASSWORD}@"
        f"{config.DATABASE_HOST}:{config.DATABASE_PORT}/{config.DATABASE_NAME}"
    )
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = Session()

    try:
        Base.metadata.create_all(session.bind)
        yield session
    finally:
        session.close()
        engine.dispose()


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True, unique=True
    )
    first_name: Mapped[str] = mapped_column(String(50))
    last_name: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(100), unique=True)
    login: Mapped[str] = mapped_column(String(50), unique=True)
    password_hash: Mapped[str] = mapped_column(String(100))
    bank_accounts: Mapped[list["BankAccount"]] = relationship(
        "BankAccount", back_populates="user"
    )


class BankAccount(Base):
    __tablename__ = "bank_accounts"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True, unique=True
    )
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    account_number: Mapped[int] = mapped_column(Integer, unique=True)
    balance: Mapped[Decimal] = mapped_column(Numeric(20, 2), default=0)
    currency: Mapped[str] = mapped_column(String(3), default="USD")
    user: Mapped["User"] = relationship("User", back_populates="bank_accounts")


class Transfers(Base):
    __tablename__ = "transfers"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True, unique=True
    )
    account_number_receiver: Mapped[int] = mapped_column(Integer)
    account_number_sender: Mapped[int] = mapped_column(Integer)
    amount: Mapped[Decimal] = mapped_column(Numeric(20, 2))
    currency: Mapped[str] = mapped_column(String(3), default="USD")


class ExchangeRate(Base):
    __tablename__ = "exchange_rates"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True, unique=True
    )
    currency: Mapped[str] = mapped_column(String(3), unique=True)
    rate: Mapped[Decimal] = mapped_column(Numeric(20, 6))


def insert_new_account_into_db(request_body: CreateBankAccountRequest, user: User):
    with db_session() as session:
        if (
            session.query(BankAccount)
            .filter_by(account_number=request_body.account_number)
            .first()
        ):
            raise Exception("Account number already exists")
        account = BankAccount(
            user_id=user.id,
            account_number=request_body.account_number,
            balance=request_body.balance,
            currency=request_body.account_currency,
        )
        session.add(account)
        session.commit()


def insert_new_transfer_into_db(request_body: TransferRequest):
    with db_session() as session:
        data = Transfers(
            account_number_receiver=request_body.account_number_receiver,
            account_number_sender=request_body.account_number_sender,
            amount=request_body.amount,
        )
        session.add(data)
        session.commit()


def check_account_exists(email: str) -> bool:
    with db_session() as session:
        rows = [row for row in session.query(User).filter(User.email == email).all()]
    return len(rows) > 0


def update_account_balance(account_id: int, amount: Decimal):
    with db_session() as session:
        account = (
            session.query(BankAccount).filter(BankAccount.id == account_id).first()
        )
        if account:
            account.balance += amount
            session.commit()


def get_currency(account_number: str) -> str:
    with db_session() as session:
        rate = (
            session.query(BankAccount)
            .filter(BankAccount.account_number == account_number)
            .first()
        )
        return str(rate.currency) if rate else None


def get_exchange_rate(currency: str) -> Decimal:
    with db_session() as session:
        rate = (
            session.query(ExchangeRate)
            .filter(ExchangeRate.currency == currency)
            .first()
        )
        return rate.rate if rate else None


def initialize_exchange_rates():
    with db_session() as session:
        if not session.query(ExchangeRate).first():
            rates = [
                ExchangeRate(currency="USD", rate=Decimal("1.0")),
                ExchangeRate(currency="EUR", rate=Decimal("0.93")),
                ExchangeRate(currency="GBP", rate=Decimal("0.80")),
                ExchangeRate(currency="JPY", rate=Decimal("151.50")),
                ExchangeRate(currency="CAD", rate=Decimal("1.36")),
                ExchangeRate(currency="KZT", rate=Decimal("515.50")),
            ]
            session.bulk_save_objects(rates)
            session.commit()


initialize_exchange_rates()
