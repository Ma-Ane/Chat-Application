# crud.py to implement various functions in the db and to interact with the db
from sqlalchemy.orm import Session
import models
from auth import hash_password

# function to return the first User with the same username
def get_user_by_username(db:Session, username:str):
    return db.query(models.User).filter(models.User.username == username).first()

# function to craete a new user
def create_user(db:Session, username:str, password:str, role:str = 'user'):
    hashed_password = hash_password(password)
    user = models.User(username=username, password=hashed_password, role=role)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def add_user_to_room(db: Session, user_id: int, room_id: int):
    # Check if user is already a member of the room
    existing = (
        db.query(models.RoomMember)
        .filter(models.RoomMember.user_id == user_id, models.RoomMember.room_id == room_id)
        .first()
    )
    if existing:
        return existing

    membership = models.RoomMember(user_id=user_id, room_id=room_id)
    db.add(membership)
    db.commit()
    db.refresh(membership)
    return membership

def remove_user_from_room(db: Session, user_id: int, room_id: int):
    membership = (
        db.query(models.RoomMember)
        .filter(models.RoomMember.user_id == user_id, models.RoomMember.room_id == room_id)
        .first()
    )
    if membership:
        db.delete(membership)
        db.commit()
        return True
    return False

def get_rooms_for_user(db: Session, user_id: int):
    return (
        db.query(models.Room)
        .join(models.RoomMember, models.Room.id == models.RoomMember.room_id)
        .filter(models.RoomMember.user_id == user_id)
        .all()
    )

