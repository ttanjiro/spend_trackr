from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    """Base class for all ORM models."""
    pass

from spendtrackr.apps.companies.models import Company  # noqa: E402, F401
from spendtrackr.apps.users.models import User  # noqa: E402, F401