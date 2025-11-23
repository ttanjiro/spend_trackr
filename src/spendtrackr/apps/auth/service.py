from sqlalchemy.orm import Session

from spendtrackr.apps.auth.schemas import SignupRequest, LoginRequest
from spendtrackr.apps.companies.models import Company
from spendtrackr.apps.users.models import User, UserRole
from spendtrackr.core.security import hash_password, verify_password, create_access_token


def signup_company_admin(db: Session, data: SignupRequest) -> tuple[Company, User, str]:
    # Create company
    company = Company(
        name=data.company_name,
        billing_email=data.company_billing_email,
    )
    db.add(company)
    db.flush()  # get company.id

    # Create admin user
    admin_user = User(
        company_id=company.id,
        email=data.admin_email,
        full_name=data.admin_full_name,
        hashed_password=hash_password(data.admin_password),
        role=UserRole.ADMIN,
    )
    db.add(admin_user)
    db.commit()
    db.refresh(company)
    db.refresh(admin_user)

    token = create_access_token(
        user_id=admin_user.id,
        company_id=company.id,
        role=admin_user.role.value,
    )

    return company, admin_user, token


def authenticate_user(db: Session, data: LoginRequest) -> tuple[Company, User, str] | None:
    # Find user by email across all companies (for MVP).
    user = db.query(User).filter(User.email == data.email).first()
    if not user:
        return None

    if not verify_password(data.password, user.hashed_password):
        return None

    if not user.is_active:
        return None

    company = db.query(Company).filter(Company.id == user.company_id).first()
    if not company:
        return None

    token = create_access_token(
        user_id=user.id,
        company_id=company.id,
        role=user.role.value,
    )

    return company, user, token
