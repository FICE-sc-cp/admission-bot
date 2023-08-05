from enum import Enum


class PaymentTypes(str, Enum):
    YEAR = "Щорічно"
    SEMESTER = "Щосеместрово"