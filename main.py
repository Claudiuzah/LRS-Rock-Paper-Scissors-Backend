import os
from typing import Annotated
import json
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

from starlette.websockets import WebSocket, WebSocketDisconnect
from websocket_manager.ws import ConnectionManager
from websocket_manager.Lobbyws import Lobbyws

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

manager = ConnectionManager()
lobby_manager = Lobbyws()


@app.websocket("/ws/{access_token}")
async def websocket_endpoint(websocket: WebSocket, access_token: str):
    lobby_id = lobby_manager.get_first_available_lobby()
    await lobby_manager.connect_to_lobby(websocket, lobby_id, access_token)

    try:
        while True:

            message = await websocket.receive_text()
            print(f"Message received from client {access_token} in lobby {lobby_id}: {message}")
            await lobby_manager.broadcast_to_lobby(lobby_id, message)

            try:
                message_data = json.loads(message)
                event = message_data.get("event")

                if event == "player ready":
                    player_data = message_data.get("data", {})
                    player_name = player_data.get("name")
                    player_ready = player_data.get("ready", False)

                    print('testulet')

                    await lobby_manager.process_player_ready(lobby_id, player_name, player_ready)

                else:
                    await lobby_manager.broadcast_to_lobby(lobby_id, message)

            except json.JSONDecodeError:
                print(f"Failed to decode JSON message: {message}")

    except WebSocketDisconnect:
        # Handle disconnection
        await lobby_manager.handle_disconnection(websocket, access_token, lobby_id)

        print(f"WebSocket connection closed for: {access_token}")


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

import uvicorn

if __name__ == "__main__":
    uvicorn.run('main:app', host='0.0.0.0', port=int(PORT),reload=True)
