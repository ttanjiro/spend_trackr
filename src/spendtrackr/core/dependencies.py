from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from spendtrackr.core.security import decode_access_token
from spendtrackr.db.session import get_db
from spendtrackr.apps.users.models import User, UserRole

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login")  # not strictly needed if we use JSON body, but okay

DBSessionDep = Annotated[Session, Depends(get_db)]
TokenDep = Annotated[str, Depends(oauth2_scheme)]


def get_current_user(
    db: DBSessionDep,
    token: TokenDep,
) -> User:
    try:
        payload = decode_access_token(token)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )

    user_id = int(payload.get("sub"))
    company_id = payload.get("company_id")

    user = (
        db.query(User)
        .filter(User.id == user_id, User.company_id == company_id, User.is_active.is_(True))
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive",
        )

    return user


def get_current_admin(
    current_user: Annotated[User, Depends(get_current_user)],
) -> User:
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required",
        )
    return current_user
