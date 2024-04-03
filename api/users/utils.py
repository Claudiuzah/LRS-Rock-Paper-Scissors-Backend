from fastapi import APIRouter
from sqlalchemy.orm import Session
# from db.models import User, GameSession
from db.session import SessionLocal
# from api.users.models import UserProfileStatistics

user_router = APIRouter(prefix="/api/user", tags=["user"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def calculate_total_points(user_id: str, db: Session) -> int:
    # calculare pct totale meciuri, update db dupa meci
    total_points = 0
    return total_points
