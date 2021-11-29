from app.models import User
from fastapi import APIRouter, Depends, status, HTTPException
from app.schemas import UserCreate, UserResponse
from typing import List
from sqlalchemy.orm import Session
from app.database import get_db
from app.utils import hash

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

## Create user
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
def create_user(user:UserCreate, db:Session = Depends(get_db)):
    username = db.query(User).filter(User.username==user.username).first()
    email = db.query(User).filter(User.email==user.email).first()
    if username:
        raise HTTPExcection(status_code=status.HTTP_409_CONFLICT, detail="user with username:{username.username} already exists")
    if email:
        raise HTTPExcection(status_code=status.HTTP_409_CONFLICT, detail="user with email:{email.email} already exists")
    hashed_password = hash(user.password)
    user.password = hashed_password
    new_user = User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

## Retrieve user detail
@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=UserResponse)
def user_detail(id:int, db:Session = Depends(get_db)):
    user = db.query(User).filter(User.id==id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'user with id:{id} not found')
    return user


