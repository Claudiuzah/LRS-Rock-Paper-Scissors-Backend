from typing import Dict
from uuid import uuid4
from db.models import session, User  # Importing the User model for querying players
from websocket_manager.ws import ConnectionManager, decode_token


class Lobbyws:
    def __init__(self):
        self.lobbies: Dict[str, dict] = {}
        self.manager = ConnectionManager()

    async def connect_to_lobby(self, websocket, lobby_id, access_token):
        if lobby_id not in self.lobbies:
            self.lobbies[lobby_id] = {"players": [], "moves": {}}

        # Disconnect previous connections with the same token
        if access_token in self.manager.active_connections:
            await self.manager.disconnect(access_token)

        # Add player to the lobby
        self.lobbies[lobby_id]["players"].append({"socket": websocket, "token": access_token})
        await self.manager.connect(websocket, access_token=access_token)

        # Broadcast updated player list to the lobby
        await self.broadcast_player_update(lobby_id)

        # Fetch all players (from DB) and online players (from active connections)
        all_players = self.get_all_players()
        online_players = self.get_online_players()

        print(f"All players from DB: {all_players}")
        print(f"Online players: {online_players}")

        # Broadcast all players to the lobby
        await self.broadcast_all_players(all_players, online_players)

        print(f"Player {access_token} connected to lobby {lobby_id}")

    async def handle_disconnection(self, websocket, access_token: str, lobby_id: str):
        if lobby_id in self.lobbies:
            players = self.lobbies[lobby_id]["players"]
            player_to_remove = next((p for p in players if p["token"] == access_token), None)

            if player_to_remove:
                players.remove(player_to_remove)
                await self.manager.disconnect(access_token)
                print(f"Player {access_token} disconnected from lobby {lobby_id}")

                # Broadcast updated player list to the lobby
                await self.broadcast_player_update(lobby_id)

                # Update and broadcast player status (all vs online)
                all_players = self.get_all_players()
                online_players = self.get_online_players()

                await self.broadcast_all_players(all_players, online_players)

            # Close the lobby if empty
            if not players:
                await self.close_lobby(lobby_id)

    async def broadcast_player_update(self, lobby_id):
        """Broadcasts player updates to the specific lobby."""
        if lobby_id in self.lobbies:
            player_tokens = [p["token"] for p in self.lobbies[lobby_id]["players"]]
            message = {"type": "playerUpdate", "players": player_tokens}

            for player in self.lobbies[lobby_id]["players"]:
                await player["socket"].send_json(message)

    async def broadcast_all_players(self, all_players, online_players):
        """Broadcasts all players (online/offline status) to all connected players."""
        for player in all_players:
            player['online'] = any(op['id'] == player['id'] for op in online_players)

        message = {
            "type": "allPlayersUpdate",
            "players": all_players
        }

        # Broadcast to all players in all lobbies
        for lobby_id, lobby_data in self.lobbies.items():
            for player in lobby_data["players"]:
                await player["socket"].send_json(message)

    def get_all_players(self):
        """Fetch all players from the database, both online and offline."""
        try:
            all_players = session.query(User).all()
            return [{"id": str(p.id), "username": p.username} for p in all_players]
        except Exception as e:
            print(f"Error fetching players: {e}")
            return []

    def get_online_players(self):
        """Return a list of currently online players."""
        online_players = []
        for lobby in self.lobbies.values():
            for player in lobby["players"]:
                username, error = decode_token(player["token"], connect_websocket=True)
                if error:
                    print(f"Error decoding token: {error}")
                    continue

                user = session.query(User).filter_by(username=username).first()
                if user:
                    online_players.append({"id": str(user.id), "username": user.username})
        return online_players

    def get_first_available_lobby(self):
        """Return the first available lobby, or create a new one."""
        for lobby_id, lobby_data in self.lobbies.items():
            if len(lobby_data["players"]) < 4:
                return lobby_id

        return self.create_lobby()

    async def close_lobby(self, lobby_id):
        """Closes the specified lobby and disconnects all players."""
        if lobby_id in self.lobbies:
            for player in self.lobbies[lobby_id]["players"]:
                try:
                    access_token = next(
                        (token for token, socket in self.manager.active_connections.items() if socket == player["socket"]),
                        None)
                    if access_token:
                        await self.manager.disconnect(access_token)
                except Exception as e:
                    print(f"Exception while closing websocket: {e}")

            del self.lobbies[lobby_id]

    async def broadcast_to_lobby(self, lobby_id: str, message: str):
        """Broadcast a text message to all players in a lobby."""
        if lobby_id in self.lobbies:
            for player in self.lobbies[lobby_id]["players"]:
                await player["socket"].send_text(message)

    def create_lobby(self):
        """Creates a new lobby and returns its ID."""
        lobby_id = str(uuid4())
        self.lobbies[lobby_id] = {"players": [], "moves": {}}
        return lobby_id

    def submit_move(self, lobby_id, access_token, move):
        """Submit a player's move in the game and determine the winner if all players have submitted."""
        if lobby_id in self.lobbies:
            self.lobbies[lobby_id]["moves"][access_token] = move
            if len(self.lobbies[lobby_id]["moves"]) == len(self.lobbies[lobby_id]["players"]):
                winner, message = self.determine_winner(self.lobbies[lobby_id]["moves"])
                return winner, message
        return None, "Waiting for other players"

    def determine_winner(self, moves: Dict[str, str]):
        """Determine the winner of the game based on the submitted moves."""
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
        """Check if a lobby has reached the maximum number of players."""
        return len(self.lobbies.get(lobby_id, {"players": []})["players"]) >= max_players
