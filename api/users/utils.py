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


# TODO
def calculate_total_points(user_id: str, db: Session) -> int:
    # calc total pts after every match
    total_points = 0
    return total_points
