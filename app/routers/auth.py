from fastapi import APIRouter, status, Depends, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.schemas import UserLogin, Token
from app.database import get_db
from  sqlalchemy.orm import Session
from app.models import User
from app.utils import verify
from app.Oauth2 import create_access_token

router = APIRouter(
    tags = ["Authentication"]
)

@router.post('/login', status_code=status.HTTP_200_OK, response_model=Token)
def user_login(user_credentials:OAuth2PasswordRequestForm = Depends(), db:Session = Depends(get_db)):
    user = db.query(User).filter(User.username == user_credentials.username).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'Invalid Credentials')
    
    if not verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Invalid Credentials')
    token = create_access_token(data={"user_id":user.id, "user_username": user.username})
    return {"access_token":token, "token_type": "bearer"}
