from typing import Optional

from pydantic import BaseModel, Field


class RegisterUser(BaseModel):
    id: int = Field(..., serialization_alias="telegramId")
    username: Optional[str] = Field(None, serialization_alias="username")
    first_name: str = Field(..., serialization_alias="firstName")
    middle_name: Optional[str] = Field(None, serialization_alias="middleName")
    last_name: str = Field(..., serialization_alias="lastName")
    phone: Optional[str] = Field(None, serialization_alias="phone")
    email: str
    speciality: str
    is_dorm: bool = Field(..., serialization_alias="isDorm")
    printed_edbo: bool = Field(..., serialization_alias="printedEdbo")
