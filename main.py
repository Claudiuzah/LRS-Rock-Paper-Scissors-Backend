from dotenv import load_dotenv

load_dotenv()
import os

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from api.lobby.lobby import lobby_router
from api.users.auth import router
from api.users.user import user_router
from db.models import SessionLocal
from api.users.auth import get_current_user
from starlette import status
from typing import Annotated
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

HOST = os.getenv("HOST")
PORT = os.getenv("PORT")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,  # pt frontend
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(lobby_router)
app.include_router(router)
app.include_router(user_router)
# app.include_router(leaderboard_router)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


@app.get("/", status_code=status.HTTP_200_OK)
async def read_root(user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication failed")
    return {"User": user}


if __name__ == "__main__":
    uvicorn.run(app, host=HOST, port=int(PORT))
    # 172.16.1.91
    # pip freeze > requirements.txt
    # pip install -r requirements.txt  For installing requirements
