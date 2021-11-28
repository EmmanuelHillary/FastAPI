from fastapi import APIRouter, Depends, status, HTTPException, Response
from typing import List, Optional
from app.schemas import PostResponse, PostCreate, PostDetail
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Post, Like
from app.Oauth2 import get_current_user
from sqlalchemy import func, desc, asc

router = APIRouter(
    prefix='/posts',
    tags=["Posts"]
)

## Create Post ##

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=PostResponse)
def post_create(post:PostCreate, db:Session = Depends(get_db), current_user:str = Depends(get_current_user)):
    print(current_user.username)
    new_post = Post(user_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

## Retrieve All Posts ##

@router.get("/", status_code=status.HTTP_200_OK, response_model=List[PostDetail]) 
def get_posts(db:Session = Depends(get_db), current_user:str = Depends(get_current_user),
                limit:int = 10, offset:int=0, search:Optional[str] = "" ):
    posts = db.query(Post, func.count(Like.post_id).label("likes")).join(Like, Like.post_id == Post.id, isouter=True).group_by(Post.id).order_by(Post.created_at.asc()).filter(Post.title.ilike(f"%{search}%")).limit(limit).offset(offset).all()
    return posts

## Retrieve Personal Posts(private) ##

@router.get('/private/{username}', status_code=status.HTTP_200_OK, response_model=List[PostDetail])
def get_personal_posts(username:str, db:Session = Depends(get_db), current_user:dict = Depends(get_current_user),
                        limit:int = 10, offset:int = 0, search:Optional[str] = ""):
    if username != current_user.username:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorised to perform requested action")
    posts = db.query(Post, func.count(Like.post_id).label("likes")).join(Like, Like.post_id == Post.id, isouter=True).group_by(Post.id).order_by(Post.created_at.asc()).filter(Post.user_id == current_user.id, Post.title.ilike(f'%{search}%')).limit(limit).offset(offset).all()
    return posts

## Retrieve Detail Post(public) ##

@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=PostDetail)
def detail_post(id:int, db:Session = Depends(get_db), current_user:str = Depends(get_current_user)):
    post = db.query(Post, func.count(Like.post_id).label("likes")).join(Like, Like.post_id==Post.id, isouter=True).group_by(Post.id).filter(Post.id==id).first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with id:{id} not found')
    return post

## Retrieve Detail Post(private) ##

@router.get('/private/{username}/{id}', status_code=status.HTTP_200_OK, response_model=PostDetail)
def get_private_posts(username:str, id:int, db:Session = Depends(get_db), current_user:dict = Depends(get_current_user)):
    if username != current_user.username:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorised to perform requested action")
    post = db.query(Post, func.count(Like.post_id).label("likes")).join(Like, Like.post_id==Post.id, isouter=True).group_by(Post.id).filter(Post.id==id).first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with id:{id} not found')
    if post[0].user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorised to perform requested action")
    return post

## Update Post
@router.put("/{id}", status_code=status.HTTP_200_OK, response_model=PostResponse)
def update_post(id:int, post:PostCreate, db:Session = Depends(get_db), current_user:str = Depends(get_current_user)):
    update_post = db.query(Post).filter(Post.id==id)
    if update_post.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with id:{id} not found')
    
    if update_post.first().user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorised to perform requested action")

    update_post.update(post.dict(), synchronize_session=False)
    db.commit()
    return update_post.first()

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int, db:Session = Depends(get_db), current_user:str = Depends(get_current_user)):
    post = db.query(Post).filter(Post.id==id)
    if post.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id:{id} not found")
    if post.first().user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorised to perform requested action")
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

    
