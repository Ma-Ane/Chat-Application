from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import crud
from authenticate.dependencies import get_current_user
from database import get_db

router = APIRouter()

@router.post("/rooms/{room_id}/join")
def join_room(room_id: int, current_user=Depends(get_current_user), db: Session=Depends(get_db)):
    membership = crud.add_user_to_room(db, current_user.id, room_id)
    if membership:
        return {"message": f"User '{current_user.username}' joined room {room_id}"}
    else:
        raise HTTPException(status_code=400, detail="Could not join the room")

@router.post("/rooms/{room_id}/leave")
def leave_room(room_id: int, current_user=Depends(get_current_user), db: Session=Depends(get_db)):
    success = crud.remove_user_from_room(db, current_user.id, room_id)
    if success:
        return {"message": f"User '{current_user.username}' left room {room_id}"}
    else:
        raise HTTPException(status_code=400, detail="Could not leave the room or not a member")

@router.get("/rooms/me")
def get_my_rooms(current_user=Depends(get_current_user), db: Session=Depends(get_db)):
    rooms = crud.get_rooms_for_user(db, current_user.id)
    return rooms
