from pydantic import BaseModel, Field


class Contract(BaseModel):
    first_name: str = Field(validation_alias="firstName")
    last_name: str = Field(validation_alias="lastName")
    middle_name: str = Field(validation_alias="middleName")
    speciality: str
    contract_number: str = Field(validation_alias="contractNumber")
    competitive_point: int = Field(validation_alias="competitivePoint")
    date: str
