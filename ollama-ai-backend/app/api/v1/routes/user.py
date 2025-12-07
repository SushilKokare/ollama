from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.models.user import User
from app.db.crud_repository import CRUDRepository
from app.schemas.user import UserCreate, UserRead

router = APIRouter(prefix="/users", tags=["Users"])
user_repo = CRUDRepository(User)

# --- Schemas for input/output (optional but recommended) ---
from pydantic import BaseModel, EmailStr


# --- Routes ---

@router.post("/", response_model=UserRead)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = user_repo.get_by_field(db, "email", user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return user_repo.create(db, user.dict())

@router.get("/{user_id}", response_model=UserRead)
def get_user(user_id: int, db: Session = Depends(get_db)):
    db_user = user_repo.get(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.get("/", response_model=List[UserRead])
def list_users(db: Session = Depends(get_db)):
    return user_repo.get_all(db)

@router.put("/{user_id}", response_model=UserRead)
def update_user(user_id: int, user: UserCreate, db: Session = Depends(get_db)):
    db_user = user_repo.get(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return user_repo.update(db, db_user, user.dict())

@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = user_repo.get(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    user_repo.delete(db, db_user)
    return {"detail": "User deleted successfully"}
