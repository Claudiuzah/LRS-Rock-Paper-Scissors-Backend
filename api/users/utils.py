from db.models import User, session
from sqlalchemy import select
import uuid


def get_user_data(user_data):
    user = session.query(User).filter_by(name=user_data.name).filter_by(password=user_data.password).first()
    if user:
        return user
    return None


def create_user(user_data):
    user = User(
        name=user_data.name,
        password=user_data.password
    )
    session.add(user)
    session.commit()
    created_user = session.query(User).filter_by(name=user_data.name).filter_by(password=user_data.password).first()
    return created_user
