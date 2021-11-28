from jose import JWTError, jwt
from datetime import datetime, timedelta
from app.schemas import TokenData
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from .config import settings


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="login"
)

ALGORITHM = settings.algorithm
SECRET_KEY = settings.secret_key
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

def create_access_token(data:dict):
    to_encode = data.copy()
    exp = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":exp})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token:str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_username = payload.get("user_username")
        if user_username is None:
            raise credentials_exception
        token_data = TokenData(username=user_username)
    except JWTError:
        raise credentials_exception
    
    return token_data

def get_current_user(token:str = Depends(oauth2_scheme), db:Session = Depends(get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
    detail="Could not validate Credentials", headers={"WWW-Authenticate": "Bearer"})
    token = verify_access_token(token, credentials_exception)
    user  = db.query(User).filter(User.username == token.username).first()
    return user
    
