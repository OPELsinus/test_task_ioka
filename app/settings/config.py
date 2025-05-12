import os
import pathlib

from dotenv import load_dotenv

load_dotenv()


class BaseConfig:

    BASE_DIR: pathlib.Path = pathlib.Path(__file__).parent.parent
    WWW_DOMAIN = "/api/dms/test-task-ioka"


class ProdConfig(BaseConfig):

    TG_TOKEN: str = os.environ.get("TG_BOT_TOKEN")
    CHAT_ID: str = os.environ.get("CHAT_ID")
    DATABASE_USER = os.environ.get("DATABASE_USER")
    DATABASE_PASSWORD = os.environ.get("DATABASE_PASSWORD")
    DATABASE_HOST = os.environ.get("DATABASE_HOST")
    DATABASE_PORT = os.environ.get("DATABASE_PORT")
    DATABASE_NAME = os.environ.get("DATABASE_NAME")


class TestConfig(BaseConfig):

    TG_TOKEN: str = os.environ.get("TG_BOT_TOKEN")
    CHAT_ID: str = os.environ.get("CHAT_ID")
    DATABASE_USER = os.environ.get("DATABASE_USER")
    DATABASE_PASSWORD = os.environ.get("DATABASE_PASSWORD")
    DATABASE_HOST = os.environ.get("DATABASE_HOST")
    DATABASE_PORT = os.environ.get("DATABASE_PORT")
    DATABASE_NAME = os.environ.get("DATABASE_NAME")


def get_settings():
    config_dict = {
        "PROD": ProdConfig,
        "TEST": TestConfig
    }

    config_name = "PROD"
    print('USING CONFIG', config_name)
    print(config_dict[config_name]())
    return config_dict[config_name]()


config = get_settings()

