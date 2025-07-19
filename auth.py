from passlib.context import CryptContext        # securely hasing
from jose import JWTError, jwt                  # create and decode JWT tokens
from datetime import datetime, timedelta


# required constants
SECRET_KEY = "super-secret-key"  # Use environment variables in production
ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# fucntion to hash the password
def hash_password(password:str):
    return pwd_context.hash(password)       # return hashed password

# function to verify the password
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# function that adds expiration to the payload and encodes JWT token 
def create_access_token(data:dict, expire_delta: timedelta=timedelta(minutes=30)):
    to_encode = data.copy()
    expire = datetime.utcnow() + expire_delta
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# function to verify token signature and decodes it
def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None         # returns None if invalid or expires
    
