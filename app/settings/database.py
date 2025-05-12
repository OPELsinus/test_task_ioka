from contextlib import contextmanager

from app.schema.request_body import CreateBankAccountRequest, TransferRequest
from app.settings.config import config

from sqlalchemy import Date, ForeignKey, Integer, Numeric, String, UUID, create_engine
from sqlalchemy.orm import Mapped, declarative_base, mapped_column, sessionmaker


Base = declarative_base()


@contextmanager
def db_session():
    """
    Context manager to handle database connection and session lifecycle.
    """
    SQLALCHEMY_DATABASE_URL = f"postgresql://{config.DATABASE_USER}:{config.DATABASE_PASSWORD}@" \
                              f"{config.DATABASE_HOST}:{config.DATABASE_PORT}/{config.DATABASE_NAME}"
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = Session()

    try:
        yield session
    finally:
        session.close()
        engine.dispose()


class Account(Base):

    __tablename__ = "accounts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, unique=True)
    first_name: Mapped[str] = mapped_column(String(50))
    last_name: Mapped[str] = mapped_column(String(50))
    account_number: Mapped[int] = mapped_column(Integer, unique=True)
    email: Mapped[str] = mapped_column(String(100), unique=True)


class Transfers(Base):

    __tablename__ = "transfers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, unique=True)
    account_number_receiver: Mapped[int] = mapped_column(Integer)
    account_number_sender: Mapped[int] = mapped_column(Integer)
    amount: Mapped[int] = mapped_column(Integer)


def insert_new_account_into_db(request_body: CreateBankAccountRequest):
    with db_session() as session:
        Base.metadata.create_all(session.bind)

        data = Account(
            first_name=request_body.holder_first_name,
            last_name=request_body.holder_last_name,
            account_number=request_body.account_number,
            email=request_body.email
        )
        session.add(data)
        session.commit()
    print('Finished adding')


def insert_new_transfer_into_db(request_body: TransferRequest):
    with db_session() as session:
        Base.metadata.create_all(session.bind)

        data = Transfers(
            account_number_receiver=request_body.account_number_receiver,
            account_number_sender=request_body.account_number_sender,
            amount=request_body.amount,
        )
        session.add(data)
        session.commit()
    print('Finished adding')


