from fastapi import APIRouter, Depends, status, Response, HTTPException
from app.schemas import LikePost
from app.models import Like, Post
from sqlalchemy.orm import Session
from app.database import get_db
from app.Oauth2 import get_current_user

router = APIRouter(
    prefix="/likes",
    tags=["Likes"]
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def like_unlike_post(post:LikePost, db:Session = Depends(get_db), current_user:dict = Depends(get_current_user)):
    post_id = post.post_id
    post = db.query(Post).filter(Post.id==post_id).first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with id:{post_id} not found')
    like = db.query(Like).filter(Like.post_id==post_id, Like.user_id==current_user.id)
    if like.first() is None:
        like_post = Like(
            user_id=current_user.id,
            post_id=post_id
        )
        db.add(like_post)
        db.commit()
        return {"message": f"User:{current_user.username} liked post of id:{post_id}"}
    else:
        like.delete(synchronize_session=False)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
