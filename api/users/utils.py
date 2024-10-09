from fastapi import APIRouter
from sqlalchemy.orm import Session
from db.session import SessionLocal

user_router = APIRouter(prefix="/api/user", tags=["user"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# TODO update points after ending a match
def calculate_total_points(user_id: str, db: Session) -> int:
    total_points = 0
    return total_points
