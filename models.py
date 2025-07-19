from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship         # used to create realtionship between tables
from datetime import datetime
from database import Base           # defined in database.py

class User(Base):
    # provide the table name 
    __tablename__ = "users"

    # define the columns in the table 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    role = Column(String, default="user")

    # each user has many messages they sent
    messages = relationship("Message", back_populates="sender")


class Message(Base):
    # create a table named 'messages'
    __tablename__ = "messages"

    # create required tables for table 'messages'
    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)
    sender_id = Column(Integer, ForeignKey("users.id"))
    room_id = Column(Integer, ForeignKey("rooms.id"))

    # message belongs to only one user
    sender = relationship("User", back_populates="messages")
    room = relationship("Room", back_populates="messages")


# room 
class Room(Base):
    __tablename__ = "rooms"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    messages = relationship("Message", back_populates="room")
