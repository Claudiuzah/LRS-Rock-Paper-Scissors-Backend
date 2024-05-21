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

    async def connect(self, websocket: WebSocket, access_token):

        if access_token in self.active_connections:
            print('Connection already established with this user')
            return await websocket.close()
        else:
            await websocket.accept()
            _, error = decode_token(access_token, SECRET_KEY, connect_websocket=True)
            self.active_connections[access_token] = websocket
            print(f"WebSocket connection established: {access_token}")

            if error:
                raise WebSocketDisconnect(code=1008, reason="Expired or invalid access token")


async def disconnect(self, access_token=None):
    self.active_connections.pop(access_token)
