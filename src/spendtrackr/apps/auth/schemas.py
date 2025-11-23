from pydantic import BaseModel, EmailStr

from spendtrackr.apps.companies.schemas import CompanyRead
from spendtrackr.apps.users.schemas import UserRead


class SignupRequest(BaseModel):
    company_name: str
    company_billing_email: EmailStr
    admin_full_name: str
    admin_email: EmailStr
    admin_password: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class MeResponse(BaseModel):
    user: UserRead
    company: CompanyRead
