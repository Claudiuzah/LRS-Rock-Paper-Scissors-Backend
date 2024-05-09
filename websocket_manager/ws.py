# from starlette.websockets import WebSocket
#
#
# class SingletonMeta(type):
#     _instances = {}
#
#     def __call__(cls, *args, **kwargs):
#         if cls in cls._instances:
#             return cls._instances[cls]
#         cls._instances[cls] = super(SingletonMeta, cls).__call__(*args, **kwargs)
#         return cls._instances[cls]
#
#
# class ConnectionManager(metaclass=SingletonMeta):
#     def __init__(self):
#         self.active_connections = {}
#
#     async def connect(self, websocket: WebSocket, client_id):
#         await websocket.accept()
#         self.active_connections[client_id] = websocket
#         await self.broadcast(message=str({"type": "active_status", "value": "Online", "user_id": client_id}))
#
#     async def broadcast(self, message: str, contacts=None):
#         pass
#
#     async def disconnect(self, client_id):
#         await self.broadcast(message=str({"type": "active_status", "value": "Offline", "user_id": client_id}))
#
#         self.active_connections.pop(client_id)

from starlette.websockets import WebSocket, WebSocketDisconnect
from uuid import UUID
from jose import JWTError, jwt

from api.users.auth import *


# auth_handler = AuthHandler()

def decode_token(token, secret=SECRET_KEY, connect_websocket=None):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload['sub'], None
    except jwt.ExpiredSignatureError:
        if connect_websocket:
            return None, 'Token has expired'
        raise HTTPException(status_code=401, detail='Token has expired')
    except jwt.InvalidTokenError as e:
        if connect_websocket:
            return None, 'Invalid token'
        raise HTTPException(status_code=401, detail='Invalid token')


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls in cls._instances:
            return cls._instances[cls]
        cls._instances[cls] = super(SingletonMeta, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class ConnectionManager(metaclass=SingletonMeta):
    def __init__(self):
        self.active_connections = {}

    async def broadcast_notification(self, user_id, notification):
        connection = None

        for token in self.active_connections:
            decoded_user_id, _ = decode_token(token, SECRET_KEY)

            if decoded_user_id == user_id:
                connection = self.active_connections.get(token)

        if connection:
            await connection.send_json(notification)

    # async def broadcast_chat_messages(self, discussion_data, message_dict):
    #     connection = None
    #     contacts = discussion_data.get("contacts")
    #     discussion_id = discussion_data.get("id")
    #
    #     for token in self.active_connections:
    #         decoded_user_id, _ = decode_token(token, SECRET_KEY)
    #
    #         if UUID(decoded_user_id) in contacts:
    #             connection = self.active_connections.get(token)
    #
    #         if connection:
    #             await connection.send_json(message_dict)
        pass

    async def connect(self, websocket: WebSocket, access_token):
        await websocket.accept()
        _, error = decode_token(access_token, SECRET_KEY, connect_websocket=True)
        self.active_connections[access_token] = websocket
        print(self.active_connections)

        if error:
            raise WebSocketDisconnect(code=1008, reason="Expired or invalid access token")

    async def disconnect(self, access_token=None):
        self.active_connections.pop(access_token)
