from typing import Optional

from sqlalchemy.orm import Mapped

from app.models import Base


class User(Base):
    __tablename__ = "users"

    first_name: Mapped[str]
    last_name: Mapped[str]
    surname: Mapped[Optional[str]]
    phone_number: Mapped[str]
    email: Mapped[str]
    dorm: Mapped[bool]
    print_edbo: Mapped[bool]
