from typing import Dict
from websocket_manager.ws import ConnectionManager



class Lobbyws:
    def __init__(self):
        self.lobbies: Dict[str, dict] = {}
        self.manager = ConnectionManager()

    async def connect_to_lobby(self, websocket, lobby_id, access_token):
        if lobby_id not in self.lobbies:
            self.lobbies[lobby_id] = {"players": [], "moves": {}}
        self.lobbies[lobby_id]["players"].append(websocket)
        await self.manager.connect(websocket, access_token=access_token)
        print(f"Player {access_token} connected to lobby {lobby_id}")

    async def close_lobby(self, lobby_id):
        if lobby_id in self.lobbies:
            players = self.lobbies[lobby_id]["players"]
            for ws in players:
                try:
                    access_token = next((token for token, socket in self.manager.active_connections.items() if socket == ws), None)
                    if access_token:
                        await self.manager.disconnect(access_token)
                except Exception as e:
                    print(f"Exception while closing websocket: {e}")
            del self.lobbies[lobby_id]

    async def broadcast_to_lobby(self, lobby_id: str, message: str):
        if lobby_id in self.lobbies:
            for ws in self.lobbies[lobby_id]["players"]:
                await ws.send_text(message)

    def get_first_available_lobby(self):
        for lobby_id, lobby_data in self.lobbies.items():
            return lobby_id
        lobby_id = generate_lobby_id()
        self.lobbies[lobby_id] = {"players": [], "moves": {}}
        return lobby_id

    def get_players_ws(self, lobby_id):
        if lobby_id in self.lobbies:
            return self.lobbies[lobby_id]["players"]
        else:
            return []

    def submit_move(self, lobby_id, access_token, move):
        if lobby_id in self.lobbies:
            self.lobbies[lobby_id]["moves"][access_token] = move
            if len(self.lobbies[lobby_id]["moves"]) == len(self.lobbies[lobby_id]["players"]):
                winner, message = self.determine_winner(self.lobbies[lobby_id]["moves"])
                return winner, message
        return None, "Waiting for other players"

    def determine_winner(self, moves: Dict[str, str]):
        # Rock-paper-scissors logic
        beats = {
            'rock': 'scissors',
            'scissors': 'paper',
            'paper': 'rock'
        }

        move_counts = {move: list(moves.values()).count(move) for move in set(moves.values())}

        if len(move_counts) == 1:
            return None, "It's a tie!"

        most_frequent_move = max(move_counts, key=move_counts.get)
        max_count = move_counts[most_frequent_move]

        if max_count == 1:
            return None, "No clear winner!"

        if all(beats[most_frequent_move] == move for move in move_counts if move != most_frequent_move):
            return most_frequent_move, f"{most_frequent_move.capitalize()} wins!"

        return None, "No clear winner!"

    def is_lobby_full(self, lobby_id, max_players=4):
        if lobby_id in self.lobbies:
            return len(self.lobbies[lobby_id]["players"]) >= max_players
        else:
            return False

# def generate_lobby_id(length=6):
#     characters = string.ascii_letters + string.digits                     TODO: change this to UUID generated idDB
#     return ''.join(random.choice(characters) for _ in range(length))