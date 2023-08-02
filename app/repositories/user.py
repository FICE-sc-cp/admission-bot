from typing import Optional

from pydantic import BaseModel

from app.models import User
from app.repositories.base import BaseRepository


class UserFilter(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    surname: Optional[str] = None


class UserRepository(BaseRepository[User, UserFilter]):
    __model__ = User
