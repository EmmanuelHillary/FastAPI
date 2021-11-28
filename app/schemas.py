from pydantic import BaseModel, EmailStr
from datetime import datetime

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = False

class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode =True

class PostCreate(PostBase):
    pass

class PostResponse(PostBase):
    id:int
    created_at: datetime
    user:UserResponse

    class Config:
        orm_mode = True

class PostDetail(BaseModel):
    Post: PostResponse
    likes: int

    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    username:str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    username:str
    password:str

class Token(BaseModel):
    access_token:str
    token_type:str

class TokenData(BaseModel):
    username:str

class LikePost(BaseModel):
    post_id:int