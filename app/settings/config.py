import os
import pathlib

from dotenv import load_dotenv

load_dotenv()


class BaseConfig:

    BASE_DIR: pathlib.Path = pathlib.Path(__file__).parent.parent
    WWW_DOMAIN = "/api/test-task-ioka"


class Localization:
    class RU:

        AccountAlreadyExists: str = "Данный счёт уже существует"
        ReceiverAccountDoesntExist: str = "Счёт получается не существует"
        SenderAccountDoesntExist: str = "Счёт отправителя не существует"

        FirstName: str = "Имя"
        LastName: str = "Фамилия"
        Username: str = "Логин"
        Password: str = "Пароль"
        Register: str = "Регистрация"
        Login: str = "Войти"
        WelcomeText: str = "Добро пожаловать"

        DashboardTitle: str = "Панель управления"
        WelcomeMessage: str = "Добро пожаловать, {name}! Вы авторизованы."
        ShowRatesBtn: str = "Показать курсы валют"
        HideRatesBtn: str = "Скрыть курсы валют"
        ExchangeRatesTitle: str = "Текущие курсы валют (1 USD)"
        CurrencyHeader: str = "Валюта"
        RateHeader: str = "Курс"
        CreateAccountTitle: str = "Создать банковский счёт"
        AccountNumberPlaceholder: str = "Номер счёта"
        InitialBalancePlaceholder: str = "Начальный баланс"
        CreateAccountBtn: str = "Создать счёт"
        ExchangeTitle: str = "Обмен валют"
        AccountFromPlaceholder = "Номер счёта списания"
        AccountToPlaceholder = "Номер счёта пополнения"
        AmountPlaceholder: str = "Сумма"
        ExchangeBtn: str = "Обменять"
        LogoutBtn: str = "Выйти"

    class EN:
        AccountAlreadyExists: str = "Account already exists"
        ReceiverAccountDoesntExist: str = "Receiver account doesn't exist"
        SenderAccountDoesntExist: str = "Sender account doesn't exist"

        FirstName: str = "Fisrt Name"
        LastName: str = "Last Name"
        Username: str = "Username"
        Password: str = "Password"
        Register: str = "Register"
        Login: str = "Login"
        WelcomeText: str = "Welcome"

        DashboardTitle: str = "Dashboard"
        WelcomeMessage: str = "Welcome, {name}! You are logged in."
        ShowRatesBtn: str = "Show Exchange Rates"
        HideRatesBtn: str = "Hide Exchange Rates"
        ExchangeRatesTitle: str = "Current Exchange Rates (1 USD)"
        CurrencyHeader: str = "Currency"
        RateHeader: str = "Rate"
        CreateAccountTitle: str = "Create Bank Account"
        AccountNumberPlaceholder: str = "Account Number"
        InitialBalancePlaceholder: str = "Initial Balance"
        CreateAccountBtn: str = "Create Account"
        ExchangeTitle: str = "Currency Exchange"
        AccountFromPlaceholder = "Account FROM Number"
        AccountToPlaceholder = "Account TO Number"
        AmountPlaceholder: str = "Amount"
        ExchangeBtn: str = "Exchange"
        LogoutBtn: str = "Logout"


class ProdConfig(BaseConfig):

    def __init__(self, lang: str = "en"):
        self.TG_TOKEN: str = os.environ.get("TG_BOT_TOKEN")
        self.CHAT_ID: str = os.environ.get("CHAT_ID")
        self.DATABASE_USER = os.environ.get("DATABASE_USER")
        self.DATABASE_PASSWORD = os.environ.get("DATABASE_PASSWORD")
        self.DATABASE_HOST = os.environ.get("DATABASE_HOST")
        self.DATABASE_PORT = os.environ.get("DATABASE_PORT")
        self.DATABASE_NAME = os.environ.get("DATABASE_NAME")
        self.SECRET_KEY = os.environ.get("SECRET_KEY")
        self.LOCALIZATION = self._get_locale(lang)

    @staticmethod
    def _get_locale(lang):
        if lang == "ru":
            return Localization.RU
        if lang == "en":
            return Localization.EN
        return Localization.EN


class TestConfig(BaseConfig):

    def __init__(self, lang: str = "en"):
        self.TG_TOKEN: str = os.environ.get("TG_BOT_TOKEN")
        self.CHAT_ID: str = os.environ.get("CHAT_ID")
        self.DATABASE_USER = os.environ.get("DATABASE_USER")
        self.DATABASE_PASSWORD = os.environ.get("DATABASE_PASSWORD")
        self.DATABASE_HOST = os.environ.get("DATABASE_HOST")
        self.DATABASE_PORT = os.environ.get("DATABASE_PORT")
        self.DATABASE_NAME = os.environ.get("DATABASE_NAME")
        self.SECRET_KEY = os.environ.get("SECRET_KEY")
        self.LOCALIZATION = self._get_locale(lang)

    @staticmethod
    def _get_locale(lang):
        if lang == "ru":
            return Localization.RU
        if lang == "en":
            return Localization.EN
        return Localization.EN


def get_settings(lang: str = "en") -> BaseConfig:
    config_dict = {"PROD": ProdConfig(lang), "TEST": TestConfig(lang)}

    config_name = "PROD"
    return config_dict[config_name]


language = "ru"
config = get_settings(lang=language)
