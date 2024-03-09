from db.models import User, session
from sqlalchemy import select
import uuid


def get_user_data(user_data):
    user = session.query(User).filter_by(name=user_data.name).filter_by(password=user_data.password).filter_by(email=user_data.email).first()
    if user:
        return user
    return None


def create_user(user_data):

    import hashlib

    password = user_data.password

    password_hash = hashlib.sha256(password.encode("utf-8")).hexdigest()
    print(f"Password Hash: {password_hash}")

    user = User(
        name=user_data.name,
        password=password_hash,
        email=user_data.email
    )
    session.add(user)
    session.commit()
    created_user = session.query(User).filter_by(name=user_data.name).filter_by(password=user_data.password).filter_by(email=user_data.email).first()
    return created_user
