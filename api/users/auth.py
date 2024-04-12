from datetime import datetime, timedelta
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from starlette import status
from db.models import SessionLocal, User
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
import os
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")


class CreateUserRequest(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, create_user_request: CreateUserRequest):
    existing_user = db.query(User).filter(User.username == create_user_request.username).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Username already exists")

    if not validate_password(create_user_request.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid password")

    create_user_model = User(
        username=create_user_request.username,
        hashed_password=bcrypt_context.hash(create_user_request.password)
    )
    db.add(create_user_model)
    db.commit()
    return {"message": "User created successfully"}


TOKEN_EXPIRATION_DAYS = 30


@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
    user = authenticate_user(username=form_data.username, password=form_data.password, db=db)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Incorrect username or password!")
    token = create_access_token(user.username, user.id, timedelta(
        days=TOKEN_EXPIRATION_DAYS))  # TODO check refresh token, token expires after a month for now
    return {"access_token": token, "token_type": "bearer"}


def authenticate_user(username: str, password: str, db):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return None
    if not bcrypt_context.verify(password, user.hashed_password):
        return None
    return user


def create_access_token(username: str, user_id: str, expires_delta: timedelta = timedelta()):
    encode = {'sub': username, 'id': str(user_id)}

    return jwt.encode(encode, SECRET_KEY)


async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: str = payload.get("id")
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user.")
        return {"username": username, "id": user_id}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user.")


user_router = APIRouter(
    prefix="/api/user",
    tags=["auth"]
)


def get_user(user_id: str, db=Depends(get_db)):
    user = db.query(User).filter_by(id=user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def validate_password(password: str) -> bool:
    if len(password) < 8:
        print(1)
        return False

    return True
