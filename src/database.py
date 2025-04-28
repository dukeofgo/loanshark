import os

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

POSTGRES_DATABASE_URL = os.environ.get("POSTGRES_DATABASE_URL")

engine = create_engine(POSTGRES_DATABASE_URL, echo=True)

Session = sessionmaker(bind=engine)

class Base(DeclarativeBase):
    pass

def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()