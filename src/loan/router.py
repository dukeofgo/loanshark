from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.database import get_db
from src.loan import crud, schemas

router = APIRouter(
    prefix="/loan",
    tags=["loan"],
)

@router.get("/",
           response_model = list[schemas.LoanResponse],
           )
def get_all_loans(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retrieve all loans from the database with pagination."""
    db_loans = crud.retrieve_all_loan(skip=skip, limit=limit, db=db)
    if not db_loans:
        raise HTTPException(status_code=404, detail="No loans found") 
    return db_loans


@router.get("/{loan_id}",
           response_model = schemas.LoanResponse,
           )
def get_loan_by_id(loan_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a certain loan based on id of loan
    """
    db_loan = crud.retrieve_loan_by_id(loan_id=loan_id, db=db)
    if not db_loan:
        raise HTTPException(status_code=404, detail="Loan not found")
    return db_loan

@router.post("/create",
             response_model = schemas.LoanResponse,
             )
async def create_loan(loan: schemas.LoanBase, db: Session = Depends(get_db)):
    """
    Create new loan
    """
    db_loan = crud.retrieve_loan_by_id(loan_id=loan.id, db=db)
    if db_loan:
        raise HTTPException(status_code=400, detail="Loan already exists")
    return await crud.create_loan(loan=loan, db=db)

@router.patch("/update/{loan_id}",
              response_model = schemas.LoanResponse,
              )
def patch_loan(loan: schemas.LoanBase, loan_id: int, db: Session = Depends(get_db)):
    """
    Update existing loan
    """
    query_loan = crud.retrieve_loan_by_id(loan_id=loan_id, db=db)
    if not query_loan:
        raise HTTPException(status_code=404, detail="Loan not found")
    return crud.update_loan(loan=loan, loan_id=loan_id, db=db)

@router.post("/callback/",
             )
def loan_callback(callback: schemas.LoanCallback, db: Session = Depends(get_db)):
    """
    Callback endpoint for loan payment confirmation.
    """
    db_loan = crud.retrieve_loan_by_id(loan_id=callback.tran_id, db=db)
    if not db_loan:
        raise HTTPException(status_code=404, detail="Loan not found")
    if callback.status == "00":
        crud.confirm_paid_status(loan_id=callback.tran_id, db=db)
    return True