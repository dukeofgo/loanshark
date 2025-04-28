from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
from src.client import models, schemas
from src.database import get_db


def retrieve_all_clients(skip: int, limit: int, db : Session = Depends(get_db)) -> list[models.Client]:
    """
    Retrieve all clients from the database with pagination.

    :param skip: Number of records to skip for pagination.
    :param limit: Maximum number of records to return.
    :param db: Database session.
    :return: Return list of clients.
    """
    return db.execute(select(models.Client).offset(skip).limit(limit)).scalars().all()


def retrieve_client_by_id(client_id: int, db: Session = Depends(get_db)) -> models.Client | None:
    """
    Retrieve certain client based on id of client

    :param client_id: Id of client
    :param db: Database session.
    :return: Return client object or None
    """
    return db.execute(select(models.Client).where(models.Client.id == client_id)).scalars().one_or_none()

def create_client(client: schemas.ClientBase, db: Session = Depends(get_db)) -> models.Client:
    """
    Create new client

    :param client: Client pydantic object
    :param db: Database Session
    :return: Return model object of client
    """
    client_dict = client.model_dump(exclude_unset=True)
    client_model = models.Client(**client_dict)
    db.add(client_model)
    db.commit()
    db.refresh(client_model)
    return client_model

def update_client(update_data: schemas.ClientBase, client_id: int, db: Session = Depends(get_db)) -> models.Client:
    """
    Update existing client

    :param update_data: pydantic object of to-be updated data
    :param client_id: Id of client
    :param db: Database session
    :return: Return updated client object
    """
    query_client = retrieve_client_by_id(client_id=client_id, db=db)
    client_dict = update_data.model_dump(exclude_unset=True)
    if client_dict:
        for key, value in client_dict.items():
            setattr(query_client, key, value)

        db.add(query_client)
        db.commit()
        db.refresh(query_client)
        return query_client
    

