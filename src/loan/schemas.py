from datetime import date
from enum import Enum

from pydantic import BaseModel


class Loan_Status(str, Enum):
    ACTIVE = "ACTIVE"
    PAID = "PAID"

class Loan_Type(str, Enum):
    PERSONAL = "PERSONAL"
    BUSINESS = "BUSINESS"
    MORTGAGE = "MORTGAGE"
    STUDENT = "STUDENT"

class Collateral_Type(str, Enum):
    REAL_ESTATE = "REAL_ESTATE"
    VEHICLE = "VEHICLE"
    EQUIPMENT = "EQUIPMENT"
    INVENTORY = "INVENTORY"
    CASH = "CASH"
    LUXURY_ITEMS = "LUXURY_ITEMS"
    COMMODITIES = "COMMODITIES"
    SECURITIES = "SECURITIES"
    COLLECTIBLES = "COLLECTIBLES"
    OTHER = "OTHER"

class LoanBase(BaseModel):
    id: int | None = None
    status: Loan_Status | None = None
    type: Loan_Type | None = None
    loan_amount: int | None = None
    disbursement_date: date | None = None
    settlement_date: date  | None = None
    collateral_type: Collateral_Type | None = None
    collateral_value: int | None = None
    client_id: int | None = None

    class config:
        orm_mode = True

class LoanResponse(LoanBase):
    client_id: int | None = None
    payment_qr_code: str | None = None

class LoanCallback(BaseModel):
    tran_id: str
    apv: int
    status: str
    merchant_ref_no: str