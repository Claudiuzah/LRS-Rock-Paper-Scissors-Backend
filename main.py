import os
from typing import Annotated

# import socketio
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from dotenv import load_dotenv

from api.lobby.lobby import lobby_router
from api.users.auth import router, get_current_user
from api.users.user import user_router
from db.models import SessionLocal
from starlette import status
from fastapi.security import OAuth2PasswordBearer
from api.leaderboard.leaderboard_top_10 import leaderboard_router

from starlette.websockets import WebSocket, WebSocketDisconnect
from websocket_manager.ws import ConnectionManager

import uvicorn

load_dotenv()

HOST = os.getenv("HOST")
PORT = os.getenv("PORT")

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(lobby_router)
app.include_router(router)
app.include_router(user_router)

app.include_router(leaderboard_router)

manager = ConnectionManager()


@app.websocket("/ws/{access_token}")
async def websocket_endpoint(websocket: WebSocket, access_token: str):
    await manager.connect(websocket, access_token=access_token)

    try:
        while True:
            message = await websocket.receive_text()
    except WebSocketDisconnect as e:
        await manager.disconnect(access_token)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


@app.get("/", status_code=status.HTTP_200_OK)
async def read_root(user: dict = Depends(get_current_user)):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication failed")
    return {"User": user}


if __name__ == "__main__":
    #     uvicorn.run(app="main:app", host=HOST, port=int(PORT), reload=True)
    #     # uvicorn.run(app="main:app", host="0.0.0.0", port=8000, reload=True)
    #     # 172.16.1.89
    #     # pip freeze > requirements.txt
    #     # pip install -r requirements.txt  For installing requirements
    import uvicorn

    uvicorn.run(app, host=HOST, port=int(PORT))
