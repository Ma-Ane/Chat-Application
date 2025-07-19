from fastapi import APIRouter, Depends
from authenticate.dependencies import get_current_active_user, get_admin_user
from models import User

router = APIRouter()

@router.get("/dashboard")
def dashboard(current_user: User = Depends(get_current_active_user)):
    return {"message": f"Welcome, {current_user.username}!"}

@router.get("/admin")
def admin_only(current_user: User = Depends(get_admin_user)):
    return {"message": f"Hello Admin {current_user.username}!"}
