from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.client import schemas
from src.database import Base


class Client(Base):
    __tablename__ = "clients"
    id: Mapped[int] = mapped_column(primary_key=True)
    status: Mapped[schemas.client_status] = mapped_column(default=schemas.client_status.ACTIVE)
    name: Mapped[str] = mapped_column(String(32))
    contact: Mapped[str] = mapped_column(String(32))
    client_banking_number: Mapped[str]
    loans: Mapped[list["Loan"]] = relationship(back_populates="client")
    number_of_loans: Mapped[int] = mapped_column(default=0)
    total_loan_amount: Mapped[int] = mapped_column(default=0)

