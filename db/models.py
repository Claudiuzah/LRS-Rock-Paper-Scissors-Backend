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
    # discussions: Mapped[List["Discussion"]] = relationship(secondary=contacts_table, back_populates="contacts")
    # messages: Mapped[List["Message"]] = relationship(back_populates="author")


    def __repr__(self):
        return {
            "id": str(self.id),
            "name": str(self.name),
            "password": str(self.password),
            "email": str(self.email)
        }


# class Discussion(Base):
#     __tablename__ = "discussion"
#
#     id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
#     contacts_ids = Column(ARRAY(UUID(as_uuid=True)), nullable=False)
#     name: Mapped[Optional[str]]
#     group_name: Mapped[Optional[str]]
#     status: Mapped[Optional[str]]
#
#     contacts: Mapped[List["User"]] = relationship(secondary=contacts_table, back_populates="discussions")
#     messages: Mapped[List["Message"]] = relationship(back_populates="discussion")
#
#     def __repr__(self):
#         return {
#             "id": str(self.id),
#             "contacts_ids": str(self.contacts_ids),
#             "name": str(self.name),
#             "group_name": str(self.group_name),
#             "status": str(self.status),
#         }


# class Message(Base):
#     __tablename__ = "message"
#
#     id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
#     discussion_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("discussion.id"))
#     user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("user.id"))
#     value: Mapped[str]
#     date: Mapped[str]
#     name: Mapped[str]
#
#     author: Mapped["User"] = relationship(back_populates="messages")
#     discussion: Mapped["Discussion"] = relationship(back_populates="messages")
#
#     def __repr__(self):
#         return {
#             "id": str(self.id),
#             "discussion_id": str(self.discussion_id),
#             "user_id": str(self.user_id),
#             "value": str(self.value),
#             "date": str(self.date),
#             "name": str(self.name),
#         }


Base.metadata.create_all(engine)
session = Session(engine)
