from datetime import datetime, timedelta
from typing import Optional

from jose import JWTError, jwt
from passlib.context import CryptContext

from spendtrackr.core.config import get_settings

settings = get_settings()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(
    user_id: int,
    company_id: int,
    role: str,
    expires_minutes: Optional[int] = None,
) -> str:
    if expires_minutes is None:
        expires_minutes = settings.access_token_expire_minutes

    expire = datetime.utcnow() + timedelta(minutes=expires_minutes)
    to_encode = {
        "sub": str(user_id),
        "company_id": company_id,
        "role": role,
        "exp": expire,
    }
    encoded_jwt = jwt.encode(
        to_encode,
        settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm,
    )
    return encoded_jwt


def decode_access_token(token: str) -> dict:
    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret_key,
            algorithms=[settings.jwt_algorithm],
        )
        return payload
    except JWTError as exc:
        raise ValueError("Invalid token") from exc
