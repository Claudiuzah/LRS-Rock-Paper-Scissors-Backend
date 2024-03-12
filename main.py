import uvicorn
from fastapi import FastAPI, status, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from starlette.websockets import WebSocket, WebSocketDisconnect
from typing import Annotated
from sqlalchemy.orm import Session
from api.lobby.lobby import lobby_router
from api.users.auth import router

# from api.websocket_manager.ws import ConnectionManager

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,  ##pt frontend
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(lobby_router)
app.include_router(router)


# manager = ConnectionManager()
#
#
# @app.websocket("/ws/{client_id}")
# async def websocket_endpoint(websocket: WebSocket, client_id: str):
#     await manager.connect(websocket, client_id)
#
#     try:
#         while True:
#             message = await websocket.receive_text()
#             await manager.broadcast(message, list(client_id))
#     except WebSocketDisconnect:
#         await manager.disconnect(websocket, client_id)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

## pip freeze > requirements.txt
## pip install -r requirements.txt  pentru instalare module
