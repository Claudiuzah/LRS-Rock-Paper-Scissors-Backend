import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.websockets import WebSocket, WebSocketDisconnect

from api.users.users import users_router
from api.websocket_manager.ws import ConnectionManager

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users_router)


manager = ConnectionManager()


@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await manager.connect(websocket, client_id)

    try:
        while True:
            message = await websocket.receive_text()
            await manager.broadcast(message, list(client_id))
    except WebSocketDisconnect:
        await manager.disconnect(websocket, client_id)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
