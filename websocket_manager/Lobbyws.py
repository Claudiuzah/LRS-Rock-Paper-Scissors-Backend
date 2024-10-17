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

        # Handle multiple connections for the same user
        if access_token in self.manager.active_connections:
            await self.manager.disconnect(access_token)  # Optionally disconnect the existing one

        self.lobbies[lobby_id]["players"].append({"socket": websocket, "token": access_token})

        # Ensure websocket connection is accepted
        await self.manager.connect(websocket, access_token=access_token)

        # Broadcast player update to the lobby
        await self.broadcast_player_update(lobby_id)

        # Fetch all players and online players
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

                # Broadcast player update to the lobby
                await self.broadcast_player_update(lobby_id)

                # Fetch all players and online players
                all_players = self.get_all_players()  # Fetch all players from DB
                online_players = self.get_online_players()  # Get the online players

                print(f"All players from DB: {all_players}")
                print(f"Online players: {online_players}")
                # Broadcast all players to the lobby
                await self.broadcast_all_players(all_players, online_players)

            # If the lobby is now empty, close it
            if len(players) == 0:
                await self.close_lobby(lobby_id)

    async def broadcast_player_update(self, lobby_id):
        if lobby_id in self.lobbies:
            players = [player["token"] for player in self.lobbies[lobby_id]["players"]]
            message = {"type": "playerUpdate", "players": players}
            for player in self.lobbies[lobby_id]["players"]:
                await player["socket"].send_json(message)

    async def broadcast_all_players(self, all_players, online_players):
        """
        Broadcasts the list of all players to the connected clients, marking which players are online.
        """
        # Mark players as online or offline
        for player in all_players:
            player['online'] = any(online_player['id'] == player['id'] for online_player in online_players)

        # Prepare the message to broadcast
        message = {
            "type": "allPlayersUpdate",
            "players": all_players  # Contains all players with their online/offline status
        }

        # Send the message to all players in all lobbies
        for lobby_id, lobby_data in self.lobbies.items():
            for player in lobby_data["players"]:
                await player["socket"].send_json(message)

    def get_all_players(self):
        """Fetch all players from the database, including both online and offline players."""
        try:
            all_players = session.query(User).all()
            player_list = [{"id": str(player.id), "username": player.username} for player in all_players]
            return player_list
        except Exception as e:
            print(f"Error fetching players: {e}")  # Fixed indentation
            return []  # Added a return statement

    def get_online_players(self):
        """Return a list of currently online players with their IDs or usernames."""
        online_players = []
        for lobby in self.lobbies.values():
            for player in lobby["players"]:
                # Decode the player's token to get the user_id from the token's payload
                username, error = decode_token(player["token"], connect_websocket=True)
                if error:
                    print(f"Error decoding token: {error}")
                    continue

                # Fetch the user from the database by user ID instead of token
                user = session.query(User).filter_by(username=username).first()
                if user:
                    online_players.append({"id": str(user.id), "username": user.username})
        return online_players

    def get_first_available_lobby(self):
        for lobby_id, lobby_data in self.lobbies.items():
            if len(lobby_data["players"]) < 4:
                return lobby_id

        lobby_id = str(uuid4())
        self.lobbies[lobby_id] = {"players": [], "moves": {}}
        return lobby_id

    async def close_lobby(self, lobby_id):
        if lobby_id in self.lobbies:
            players = self.lobbies[lobby_id]["players"]
            for ws in players:
                try:
                    access_token = next(
                        (token for token, socket in self.manager.active_connections.items() if socket == ws["socket"]),
                        None)
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

    def is_lobby_full(self, lobby_id, max_players=4):
        if lobby_id in self.lobbies:
            return len(self.lobbies[lobby_id]["players"]) >= max_players
        else:
            return False
