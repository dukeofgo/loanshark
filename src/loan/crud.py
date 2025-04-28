from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
from src.database import get_db
from src.loan import models, schemas, utils, schemas

def retrieve_all_loan(skip: int, limit: int, db: Session = Depends(get_db)) -> list[models.Loan]:
    """
    Retrive all existing loans from database

    :param skip: Number of records to skip
    :param limit: Number of records to return
    :param db: Database session
    :return: List of Loan objects
    """
    return db.execute(select(models.Loan).offset(skip).limit(limit)).scalars().all()

def retrieve_loan_by_id(loan_id: str, db: Session = Depends(get_db)) -> models.Loan:
    """
    Retrive individual loan using loan's id from database

    :param loan_id: Loan id
    :param db: Database session
    :return: Loan object
    """
    return db.execute(select(models.Loan).where(models.Loan.id == loan_id)).scalars().one_or_none()

def retrieve_loan_qr(db: Session = Depends(get_db)) -> list[tuple[int, str, schemas.Loan_Status]]:
    """
    Retrieve QR codes of all loans
    
    :param db: Database session
    :return: List of tuples containing loan id, payment qr code and status
    """
    return db.execute(select(models.Loan.id, models.Loan.payment_qr_code, models.Loan.status)).all()

async def create_loan(loan: schemas.LoanBase, db: Session = Depends(get_db)) -> bool:
    """
    Create a new loan in database

    :param loan: Pydantic object of loan
    :param db: Database session
    :return: True if loan is created successfully
    """
    
    loan_dict = loan.model_dump(exclude_unset=True)
    loan_model = models.Loan(**loan_dict)

    db.add(loan_model)
    db.flush() # flushing db, so that we have loan's id to work with

    # Generate QR string
    qr_string = await utils.generate_qr_code(loan_model)
    setattr(loan_model, "payment_qr_code", qr_string)

    db.commit()
    db.refresh(loan_model)
    return loan_model

def update_loan(loan: schemas.LoanBase, loan_id: int, db: Session = Depends(get_db)) -> bool:
    """
    Update an existing loan in database

    :param loan: Pydantic object of loan
    :param loan_id: Loan id
    :param db: Database session
    :return: True if loan is created successfully
    """
    query_loan = retrieve_loan_by_id(loan_id=loan_id, db=db)
    update_data = loan.model_dump(exclude_unset=True)
    print(update_data)
    if update_data:
        for key, value in update_data.items():
            setattr(query_loan, key, value)

        db.add(query_loan)
        db.commit()
        db.refresh(query_loan)
        return query_loan

def confirm_paid_status(loan_id: int, db: Session = Depends(get_db)) -> bool:
    """
    Confirm paid status of loan

    :param loan_id: Loan id
    :param db: Database session
    :return: True if loan is paid
    """
    query_loan = retrieve_loan_by_id(loan_id=loan_id, db=db)

    if query_loan.status == schemas.Loan_Status.ACTIVE:
        setattr(query_loan, "status", schemas.Loan_Status.PAID)

    db.add(query_loan)
    db.commit()
    db.refresh(query_loan)

    return True



