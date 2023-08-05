from typing import Optional, Union

from pydantic import BaseModel, Field


class Contract(BaseModel):
    first_name: str = Field(validation_alias="firstName")
    last_name: str = Field(validation_alias="lastName")
    middle_name: Optional[str] = Field(None, validation_alias="middleName")
    speciality: Optional[str] = Field(None, validation_alias="specialty")
    contract_number: Optional[str] = Field(None, validation_alias="contractNumber")
    competitive_point: Optional[Union[int, float]] = Field(None, validation_alias="competitivePoint")
    date: Optional[str] = Field(None)
