from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from database import get_db
from models import User
from auth import SECRET_KEY, ALGORITHM

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# decode the jwt toekn and get the user from db 
def get_current_user(token:str=Depends(oauth2_scheme), db:Session=Depends(get_db)):
    
    # Handle credential error
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail = 'Could not validate credential',
        headers={"WWW-Authenticate": "Bearer"}
    )

    # decode the token and search for payload
    try:
        payload = jwt.decode(token, SECRET_KEY, [ALGORITHM])
        print("Payload:", payload)
        username:str = payload.get('username')
        role: str = payload.get("role")

        if username is None or role is None:
            print("Missing username or role in token")
            raise credential_exception
        
    except JWTError as e:
        print("JWT Error:", e)
        raise credential_exception
    
    # query the user with the usename
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise credential_exception
    
    return user

# used to check if user is logged in
def get_current_active_user(current_user:User=Depends(get_current_user)):
    return current_user

# check if current user has admin role
def get_admin_user(current_user:User=Depends(get_current_user)):
    print("User role:", current_user.role)  # Debug print
    if current_user.role != 'admin':
        raise HTTPException(status_code=403, detail='Admin only!')

    return current_user

