from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime


class BaseDataSchema(BaseModel):
    id: str
    userId: str
    firstName: str
    middleName: Optional[str] = None
    lastName: str
    email: str
    passportSeries: str
    passportNumber: str
    passportInstitute: str
    passportDate: str
    phoneNumber: str
    idCode: str
    region: str
    settlement: str
    address: str
    index: str
    createdAt: datetime
    updatedAt: datetime


class PrioritySchema(BaseModel):
    contractId: str
    number: int
    program: str
    createdAt: datetime
    updatedAt: datetime


class ContractSchema(BaseModel):
    id: str
    state: str
    number: str
    date: str
    degree: str
    educationalProgram: str
    programType: str
    paymentType: str
    specialty: str
    studyForm: str
    fundingSource: str
    priorityState: str
    priorityDate: str
    userId: str
    createdAt: datetime
    updatedAt: datetime
    priorities: List[PrioritySchema]


class EntrantDataSchema(BaseDataSchema):
    pass


class RepresentativeDataSchema(BaseDataSchema):
    pass


class CustomerDataSchema(BaseDataSchema):
    pass


class UserSchema(BaseModel):
    model_config = ConfigDict(extra='ignore')

    id: str
    email: str
    first_name: str = Field(validation_alias="firstName")
    middle_name: Optional[str] = Field(None, validation_alias="middleName")
    last_name: str = Field(validation_alias="lastName")
    telegram_id: Optional[str] = Field(None, validation_alias="telegramId")
    phone: str
    is_dorm: bool
    printed_edbo: bool = Field(validation_alias="printedEdbo")
    expected_specialities: str = Field(validation_alias="expectedSpecialities")
