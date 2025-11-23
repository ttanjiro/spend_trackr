from datetime import datetime

from pydantic import BaseModel, EmailStr


class CompanyBase(BaseModel):
    name: str
    billing_email: EmailStr


class CompanyCreate(CompanyBase):
    pass


class CompanyRead(CompanyBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True  # for ORM mode in Pydantic v2
