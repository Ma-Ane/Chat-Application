# schemas.py for request/response schemas
from pydantic import BaseModel

# class for creating a user
class UserCreate(BaseModel):
    username: str
    password: str
    role: str = "user"

# class for required values for logging in
class UserLogin(BaseModel):
    username: str
    password: str

# class for managinf tokens
class TokenData(BaseModel):
    username: str
    role: str
