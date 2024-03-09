from starlette.websockets import WebSocket

from db.models import session, User


class SingletonMeta(type):
    """
    A Singleton metaclass that creates a Singleton instance.
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        """
        If an instance of the class doesn't exist, create one. Otherwise, return the existing instance.
        """
        if cls not in cls._instances:
            cls._instances[cls] = super(SingletonMeta, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class ConnectionManager(metaclass=SingletonMeta):
    def __init__(self):
        self.active_connections: {} = {}

    async def connect(self, websocket: WebSocket, client_id: str):
        await websocket.accept()
        self.active_connections[client_id] = websocket

    async def disconnect(self, websocket: WebSocket, client_id):
        self.active_connections.pop(client_id)

    # async def broadcast(self, message: str, users):
    #     for contact_id in users:
    #         connection = self.active_connections.get(contact_id)
    #         if connection:
    #             await connection.send_text(message)
