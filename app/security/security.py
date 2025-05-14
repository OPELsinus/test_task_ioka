from datetime import datetime, timedelta
from typing import Optional
import hashlib

from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer, HTTPBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

from app.settings.config import config
from app.settings.database import User, db_session

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 5


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


security = HTTPBearer()
pwd_context = CryptContext(schemes=["sha256_crypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def verify_password(plain_password: str, hashed_password: str):
    return hashlib.sha256(plain_password.encode()).hexdigest() == hashed_password


def get_password_hash(password: str):
    return hashlib.sha256(password.encode()).hexdigest()


def create_access_token(data: dict):
    return jwt.encode(data, config.SECRET_KEY, algorithm="HS256")


def verify_token(token: str):
    try:
        return jwt.decode(token, "SECRET_KEY", algorithms=["HS256"])
    except:
        return None


async def get_current_user(request: Request):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid authentication credentials",
    )

    token = request.cookies.get("access_token")
    if not token:
        raise credentials_exception

    try:
        token = token.replace("Bearer ", "")
        payload = jwt.decode(token, config.SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if not username:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    with db_session() as session:
        user = session.query(User).filter(User.login == username).first()
        if not user:
            raise credentials_exception
        return user
