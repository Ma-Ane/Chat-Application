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

