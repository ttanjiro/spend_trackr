from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from fastapi.security import OAuth2PasswordRequestForm
from spendtrackr.apps.auth.schemas import SignupRequest, LoginRequest, TokenResponse, MeResponse
from spendtrackr.apps.companies.schemas import CompanyRead
from spendtrackr.apps.users.schemas import UserRead
from spendtrackr.core.dependencies import DBSessionDep, get_current_user
from spendtrackr.db.session import get_db

from . import service as auth_service

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/signup", response_model=TokenResponse)
def signup(
    payload: SignupRequest,
    db: DBSessionDep,
):
    company, admin_user, token = auth_service.signup_company_admin(db, payload)
    return TokenResponse(access_token=token)


@router.post("/login", response_model=TokenResponse)
def login(
    db: DBSessionDep,
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    payload = LoginRequest(
        email=form_data.username,
        password=form_data.password,
    )
    result = auth_service.authenticate_user(db, payload)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )

    company, user, token = result
    return TokenResponse(access_token=token)


@router.get("/me", response_model=MeResponse)
def me(
    db: DBSessionDep,
    current_user=Depends(get_current_user),
):
    # reload company to be safe
    from spendtrackr.apps.companies.models import Company

    company = db.query(Company).filter(Company.id == current_user.company_id).first()
    return MeResponse(
        user=current_user,
        company=company,
    )
