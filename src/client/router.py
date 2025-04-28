
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.client import crud, schemas
from src.database import get_db

router = APIRouter(
    prefix="/client",
    tags=["client"],
)

@router.get("/",
           response_model = list[schemas.ClientBase],)
def get_all_clients(skip: int = 0, limit: int = 100, db : Session = Depends(get_db)):
    """
    Retrieve all clients from the database with pagination.
    """
    db_clients = crud.retrieve_all_clients(skip=skip, limit=limit, db=db)
    if not db_clients:
        raise HTTPException(status_code=404, detail="clients are not found")
    return db_clients

@router.get("/{client_id}",
           response_model = schemas.ClientBase,)
def get_client_by_id(client_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a certain client based on id of client
    """
    db_client = crud.retrieve_client_by_id(client_id=client_id, db=db)
    if not db_client:
        raise HTTPException(status_code=404, detail="client does not exist")
    return db_client

@router.post("/create", 
             response_model = schemas.ClientBase,)
def create_client(client: schemas.ClientBase, db: Session = Depends(get_db)):
    """
    Create new client
    """
    db_client = crud.retrieve_client_by_id(client_id=client.id, db=db)
    if db_client:
        raise HTTPException(status_code=400, detail="client already exists")
    return crud.create_client(client=client, db=db)
    
@router.patch("/update/{client_id}",
             response_model = schemas.ClientBase,)
def update_client(client_id: int, client: schemas.ClientBase, db: Session = Depends(get_db)):
    """"
    Update existing client
    """
    db_client = crud.retrieve_client_by_id(client_id=client_id, db=db)
    if not db_client:
        raise HTTPException(status_code=404, detail="client does not exist")
    return crud.update_client(update_data=client, client_id=client_id, db=db)
    