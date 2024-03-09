from datetime import datetime

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, Session
from sqlalchemy import ForeignKey, Table, Column, create_engine, ARRAY, UUID
from typing import List, Optional

import uuid

engine = create_engine("postgresql://postgres:1234@localhost:5432/RPSDB")


class Base(DeclarativeBase):
    pass


# contacts_table = Table(
#     "contacts_table",
#     Base.metadata,
#     Column("discussion_id", ForeignKey("discussion.id")),
#     Column("user_id", ForeignKey("user.id"))
# )


class User(Base):
    __tablename__ = "user"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    name: Mapped[str]
    password: Mapped[str]
    email: Mapped[str]

    def __repr__(self):
        return {
            "id": str(self.id),
            "name": str(self.name),
            "password": str(self.password),
            "email": str(self.email)
        }


class GameSession(Base):
    __tablename__ = "game_session"
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    lobby_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("lobby.id"))
    winner_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("user.id"))
    start_time: Mapped[str]
    end_time: Mapped[str]

    def __repr__(self):
        return {
            "id": str(self.id),
            "lobby_id": str(self.lobby_id),
            "winner_id": str(self.winner_id),
            "start_time": str(self.start_time),
            "end_time": str(self.end_time)
        }


class Lobby(Base):
    __tablename__ = "lobby"
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    lobby_name: Mapped[str]
    rounds: Mapped[int]

    def __repr__(self):
        return {
            "id": str(self.id),
            "lobby_name": str(self.lobby_name),
            "rounds": str(self.rounds)
        }


class Move(Base):
    __tablename__ = "move"
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    session_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("game_session.id"))
    player_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("user.id"))
    choice: Mapped[str] = mapped_column()

    def __repr__(self):
        return {
            "id": str(self.id),
            "session_id": str(self.session_id),
            "player_id": str(self.player_id),
            "choice": str(self)
        }

class History(Base):
    __tablename__ = "history"
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    player_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("user.id"))
    opponent_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("user.id"))



class UserLobby(Base):
    __tablename__ = "user_lobby"
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("user.id"))
    lobby_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("lobby.id"))


Base.metadata.create_all(engine)
session = Session(engine)

###TREBUIE RECONFIGURAT DUPA ERD UL NOU
## posibil local cache pentru history

# import hashlib
#
# password = input("Password: ")
# password_hash = hashlib.sha256(password.encode("utf-8")).hexdigest()
# print(f"Password Hash: {password_hash}")