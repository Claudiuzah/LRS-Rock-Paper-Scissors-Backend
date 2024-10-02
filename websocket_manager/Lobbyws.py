from typing import Dict
from uuid import uuid4
from websocket_manager.ws import ConnectionManager


class Lobbyws:
    def __init__(self):
        self.lobbies: Dict[str, dict] = {}
        self.manager = ConnectionManager()

    async def connect_to_lobby(self, websocket, access_token):
        # Get an available lobby for the player
        lobby_id = self.get_first_available_lobby()

        # Handle multiple connections for the same user
        if access_token in self.manager.active_connections:
            await self.manager.disconnect(access_token)  # Optionally disconnect the existing one

        self.lobbies[lobby_id]["players"].append({"socket": websocket, "token": access_token})

        # Ensure websocket connection is accepted
        await self.manager.connect(websocket, access_token=access_token)

        print(f"Player {access_token} connected to lobby {lobby_id}")

    async def handle_disconnection(self, websocket, access_token: str, lobby_id: str):
        if lobby_id in self.lobbies:
            players = self.lobbies[lobby_id]["players"]
            player_to_remove = None

            # Find the player in the lobby based on their access token
            for player in players:
                if player["token"] == access_token:
                    player_to_remove = player
                    break

            # If the player was found, remove them from the lobby
            if player_to_remove:
                players.remove(player_to_remove)
                await self.manager.disconnect(access_token)
                print(f"Player {access_token} disconnected from lobby {lobby_id}")

            # If the lobby is now empty, close it
            if len(players) == 0:
                await self.close_lobby(lobby_id)

    def get_first_available_lobby(self):
        # Look for existing lobbies with less than 2 players
        for lobby_id, lobby_data in self.lobbies.items():
            if len(lobby_data["players"]) < 2:  # Adjust this number as needed
                return lobby_id

        # If no existing lobby is found, create a new one
        lobby_id = str(uuid4())
        self.lobbies[lobby_id] = {"players": [], "moves": {}}
        return lobby_id

    async def close_lobby(self, lobby_id):
        if lobby_id in self.lobbies:
            players = self.lobbies[lobby_id]["players"]
            for ws in players:
                try:
                    access_token = next(
                        (token for token, socket in self.manager.active_connections.items() if socket == ws["socket"]), None)
                    if access_token:
                        await self.manager.disconnect(access_token)
                except Exception as e:
                    print(f"Exception while closing websocket: {e}")
            del self.lobbies[lobby_id]

    async def broadcast_to_lobby(self, lobby_id: str, message: str):
        if lobby_id in self.lobbies:
            for player in self.lobbies[lobby_id]["players"]:
                await player["socket"].send_text(message)

    def create_lobby(self):
        lobby_id = str(uuid4())
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

    def is_lobby_full(self, lobby_id, max_players=6):
        if lobby_id in self.lobbies:
            return len(self.lobbies[lobby_id]["players"]) >= max_players
        else:
            return False
