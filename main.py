# import required packages
from fastapi import FastAPI, Depends, HTTPException, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
import models, schemas, crud
from database import engine, SessionLocal, get_db
from auth import verify_password, create_access_token, SECRET_KEY, ALGORITHM
from routes import protected
from authenticate.dependencies import get_current_user, get_admin_user
from jose import jwt, JWTError
from datetime import datetime
import json
from routes import rooms  # Import the new router


# make an instance of fast api
app = FastAPI()

# Include user router
app.include_router(protected.router, prefix="/protected", tags=["Users"])

# Include room router
app.include_router(rooms.router, prefix="/rooms", tags=["Rooms"])

# Create the tables when app starts
models.Base.metadata.create_all(bind=engine)

# dictionary to track clients in a room
connected_clients = {}  


# root directory
@app.get("/")
def read_root():
    return {"message": "Home Page!"}

# verify token for connection
async def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("username")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return username
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")



# create a signup page
@app.post('/signup')
def signup(user:schemas.UserCreate, db:Session=Depends(get_db)):

    # check if user already existed
    db_user = crud.get_user_by_username(db, user.username)
    if db_user:
        raise HTTPException(status_code=400, detail='Username already registered')
    
    # if no user, create a new one
    new_user = crud.create_user(db, user.username, user.password, user.role)
    return {'message': 'User created', 'username': new_user.username, 'role': new_user.role}


# Log in using the credentials
@app.post('/login')
def login(form_data: OAuth2PasswordRequestForm=Depends(), db:Session=Depends(get_db)):
    
    # get data from the database 
    user = crud.get_user_by_username(db, form_data.username)
    
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=401, detail='Invalid credentials')
    
    token = create_access_token({'username': user.username, 'role': user.role})
    return {'access_token': token, 'token_type': 'bearer'}


# get the dashboard
@app.get("/dashboard")
def dashboard(current_user: dict = Depends(get_current_user)):
    return {"message": f"Welcome {current_user['username']}!"}


# admin-only page
@app.get("/admin")
def admin_dashboard(admin_user = Depends(get_admin_user)):
    return {"message": f"Welcome Admin {admin_user.username}!"}


# create a roon id to test
@app.on_event("startup")
def create_test_room():
    db = SessionLocal()
    room = db.query(models.Room).filter_by(id=1).first()
    if not room:
        room = models.Room(id=1, name="Test Room")
        db.add(room)
        db.commit()
    db.close()


# websocket with room id
@app.websocket("/ws/{room_id}")
async def websocket_endpoint(websocket: WebSocket, room_id: int, db: Session = Depends(get_db)):
    print("WebSocket connection attempt:", room_id)
    token = websocket.query_params.get("token")
    if not token:
        print("Missing token")
        await websocket.accept()
        await websocket.send_text("ERROR: Token is missing.")
        await websocket.close(code=1008)
        return

    try:
        username = await verify_token(token)
        print("Verified username:", username)

        user = crud.get_user_by_username(db, username)
        print("User from DB:", user)

        if not user:
            print("User not found")
            await websocket.accept()
            await websocket.send_text("ERROR: User not found.")
            await websocket.close(code=1008)
            return

    except Exception as e:
        print("Token verification or user fetch error:", e)
        await websocket.accept()
        await websocket.send_text(f"ERROR: {str(e)}")
        await websocket.close(code=1008)
        return

    room = db.query(models.Room).filter(models.Room.id == room_id).first()
    if not room:
        print("Room not found")
        await websocket.accept()
        await websocket.send_text("ERROR: Room not found.")
        await websocket.close(code=1008)
        return

    is_member = (
        db.query(models.RoomMember)
        .filter_by(room_id=room_id, user_id=user.id)
        .first()
    )
    if not is_member:
        print(f"User {user.username} not a member of room {room_id}")
        await websocket.accept()
        await websocket.send_text("ERROR: You are not a member of this room.")
        await websocket.close(code=1008)
        return

    print("Accepting websocket connection")
    await websocket.accept()

    try:
        recent_messages = (
            db.query(models.Message)
            .filter(models.Message.room_id == room_id)
            .order_by(models.Message.timestamp.desc())
            .limit(10)
            .all()
        )

        for msg in reversed(recent_messages):
            sender = db.query(models.User).filter(models.User.id == msg.sender_id).first()
            sender_name = sender.username if sender else "Unknown"
            await websocket.send_text(json.dumps({
                "id": msg.id,
                "content": msg.content,
                "timestamp": msg.timestamp.isoformat(),
                "sender": sender_name,
                "room_id": msg.room_id
            }))

        if room_id not in connected_clients:
            connected_clients[room_id] = set()
        connected_clients[room_id].add(websocket)

        print(f"User {user.username} connected to room {room_id}")

        while True:
            data = await websocket.receive_text()
            print(f"Received data from {user.username}: {data}")
            message_data = json.loads(data)
            content = message_data.get("content")

            new_message = models.Message(
                content=content,
                timestamp=datetime.utcnow(),
                sender_id=user.id,
                room_id=room_id
            )
            db.add(new_message)
            db.commit()
            db.refresh(new_message)

            formatted_msg = {
                "id": new_message.id,
                "content": new_message.content,
                "timestamp": new_message.timestamp.isoformat(),
                "sender": user.username,
                "room_id": new_message.room_id
            }

            for client in connected_clients[room_id]:
                await client.send_text(json.dumps(formatted_msg))

    except WebSocketDisconnect:
        print(f"User {user.username} disconnected from room {room_id}")
        connected_clients[room_id].remove(websocket)
        if not connected_clients[room_id]:
            del connected_clients[room_id]
    except Exception as e:
        print(f"Unexpected error: {e}")
        await websocket.close(code=1011)



# get the lists of the rooms avalilable
@app.get("/rooms")
def get_rooms(db: Session = Depends(get_db)):
    return db.query(models.Room).all()


# add user to the room
# @app.post("/rooms/{room_id}/join")
# def join_room(room_id: int, current_user=Depends(get_current_user), db: Session=Depends(get_db)):
#     membership = crud.add_user_to_room(db, current_user.id, room_id)
#     if membership:
#         return {"message": f"User '{current_user.username}' joined room {room_id}"}
#     else:
#         raise HTTPException(status_code=400, detail="Could not join the room")