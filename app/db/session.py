from sqlmodel import Session
from app.db.engine import engine

def get_session():
    with Session(engine) as session:
        yield session
