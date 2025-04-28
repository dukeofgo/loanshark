from datetime import date

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database import Base
from src.loan.schemas import Collateral_Type, Loan_Status, Loan_Type


class Loan(Base):
    __tablename__ = "loans"
    id: Mapped[int] = mapped_column(primary_key=True)
    status: Mapped[Loan_Status] = mapped_column(default=Loan_Status.ACTIVE)
    type: Mapped[Loan_Type]
    loan_amount: Mapped[int]
    disbursement_date: Mapped[date] = mapped_column(default=date.today())
    settlement_date: Mapped[date] = mapped_column(nullable=True)
    collateral_type: Mapped[Collateral_Type] = mapped_column(nullable=True)
    collateral_value: Mapped[int] = mapped_column(nullable=True)
    client_id: Mapped[int] = mapped_column(ForeignKey("clients.id"))
    client: Mapped["Client"] = relationship(back_populates="loans")
    payment_qr_code: Mapped[str] = mapped_column(nullable=True)

