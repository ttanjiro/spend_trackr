from datetime import datetime
from typing import Literal

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    full_name: str
    email: EmailStr


class UserCreate(UserBase):
    password: str
    role: Literal["ADMIN", "EMPLOYEE"] = "EMPLOYEE"


class UserRead(UserBase):
    id: int
    company_id: int
    role: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True
