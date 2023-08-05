from typing import Optional

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import BigInteger

from app.models import Base


class User(Base):
    __tablename__ = "queue_users"

    telegram_id: Mapped[int] = mapped_column(BigInteger)
    first_name: Mapped[str]
    last_name: Mapped[str]
    surname: Mapped[Optional[str]]
    username: Mapped[Optional[str]]
    phone: Mapped[str]
    email: Mapped[str]
    speciality: Mapped[str]
    is_dorm: Mapped[bool]
    study_form: Mapped[str] = mapped_column(server_default="Денна")
    study_type: Mapped[str] = mapped_column(server_default="Бюджет")
    payment_type: Mapped[Optional[str]]
    confirm_edbo: Mapped[bool] = mapped_column(server_default="0")
    printed_edbo: Mapped[Optional[bool]]
