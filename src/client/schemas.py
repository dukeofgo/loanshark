from enum import Enum
from pydantic import BaseModel

class client_status(str, Enum):
    INACTIVE = "INACTIVE"
    ACTIVE = "ACTIVE"
    
    
class ClientBase(BaseModel):
    id: int | None = None
    status: client_status | None = None
    name: str | None = None
    contact: str | None = None
    client_banking_number: str | None = None
    number_of_loans: int | None = None
    total_loan_amount: int | None = None

    class Config:
        orm_mode = True
