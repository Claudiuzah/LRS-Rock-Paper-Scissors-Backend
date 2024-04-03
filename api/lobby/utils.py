from db.models import SessionLocal
from db.models import User
from fastapi import APIRouter, Depends, HTTPException


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_lobby_data(db=Depends(get_db)):
    lobby_data = db.query(User).filter_by(id=user_id).first()


def create_lobby():
    pass
