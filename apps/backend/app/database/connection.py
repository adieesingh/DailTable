from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker,Session
from collections.abc import Generator

DATABASE_URL = "postgresql+psycopg://postgres:root@localhost:5432/dailtable"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    bind= engine,
    autoflush= False,
    autocommit=False        
)

class Base(DeclarativeBase):
    pass

def get_db()-> Generator[Session,None,None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()