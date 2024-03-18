from datetime import datetime, timedelta
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from starlette import status
from db.models import SessionLocal
from db.models import User
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

SECRET_KEY = "secret"  # TODO: change this to a real secret key :)
ALGORITHM = 'HS256'

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


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency,
                      create_user_request: CreateUserRequest):
    create_user_model = User(
        username=create_user_request.username,
        hashed_password=bcrypt_context.hash(create_user_request.password)
    )
    db.add(create_user_model)
    db.commit()


@router.post("/token", response_model=Token)  # login token
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                                 db: db_dependency):
    user = authenticate_user(username=form_data.username, password=form_data.password, db=db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Incorrect username or password/Could not validate user.")
    token = create_access_token(user.username, user.id, timedelta(days=30))  # TODO check refresh token, token expires after a month for now
    return {"access_token": token, "token_type": "bearer"}


def authenticate_user(username: str, password: str, db):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
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


@user_router.get('/{user_id}')
def get_user(user_id: str, db=Depends(get_db)):
    user = db.query(User).filter_by(id=user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# @user_router.get('/active') # TODO: add offline user
# async def get_current_active_user(current_user: User = Depends(get_current_user)):
#     if current_user.offline:
#         raise HTTPException(status_code=400, detail="Inactive user")
#     return current_user


# class UserUpdate(BaseModel):
#     username: str
#     ##TODO: add customisable profile
# @user_router.put('/{user_id}')
# def update_user(user_id: str, user_update: UserUpdate, db = Depends(get_db)):
#     # Check if user exists
#     user = db.query(User).filter_by(id=user_id).first()
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")
#
#     # Update user data
#     update_values = {"username": user_update.username}
#     query = user.update().where(user.c.id == user_id).values(**update_values)
#     db.execute(query)
#     db.commit()
#
#     return {"message": "User updated successfully"} NU MERGE DEOCAMDATA

