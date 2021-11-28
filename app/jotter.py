### Extras ###    
# from fastapi import FastAPI, Response, status, HTTPException, Depends
# from pydantic import BaseModel
# from typing import Optional, List
# from random import randrange
# import psycopg2
# from psycopg2.extras import RealDictCursor
# import time
# from sqlalchemy.orm import Session
# from . import models
# from . import schemas
# from .database import engine, get_db
# from .utils import hash
# from fastapi.params import Body

# app = FastAPI()

# receiving mdata from the frontend without schemas

# @app.post("/post/create")
# def create_posts(payload: dict = Body(...)):
#     return {"data": payload}

# raising HTTP errors

# @app.get("/posts/{id}")
# def get_post_detail(id:int, response:Response):
#     post = find_post(id)
#     if not post:
#         response.status_code = status.HTTP_404_NOT_FOUND
#         return {"message": f'post with id:{id} not found'} 
#     return {"data": post}
#
# CRUD Functionalities using SQL statements

# while True:
#     try:
#         conn = psycopg2.connect(host='localhost',database='FastAPI',user='postgres',password="Nintendo1.",
#             cursor_factory=RealDictCursor
#         )
#         cursor = conn.cursor()
#         print("Succesfully Connected to the Database")
#         break
#     except Exception as error:
#         print("Failed to Connect to the Database")
#         print("Error:", error)
#         time.sleep(3) 

# @app.get("/posts", status_code=status.HTTP_200_OK)
# def get_posts():
#     cursor.execute("SELECT * FROM posts;")
#     posts = cursor.fetchall()
#     return {"data": posts}

# @app.post("/posts", status_code=status.HTTP_201_CREATED)
# def create_posts(post:Post):
#     cursor.execute("INSERT INTO posts(title, content, published) VALUES (%s, %s, %s) RETURNING *;", 
#                                                                 (post.title, post.content, post.published))
#     new_post = cursor.fetchone()
#     conn.commit()
    
#     return {"data": new_post} 

# @app.get("/posts/{id}")
# def get_post_detail(id:int):
#     post_id = str(id)
#     cursor.execute("""SELECT * FROM posts WHERE id = %s;""", (post_id,))
#     post = cursor.fetchone()
#     if post is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with id:{id} not found')
#     return {"data": post}

# @app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
# def delete_post(id:int):
#     post_id = str(id)
#     cursor.execute("DELETE FROM posts WHERE id=%s RETURNING *", (post_id,))
#     post = cursor.fetchone()
#     conn.commit()
#     if post is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id:{id} not found")
#     return Response(status_code=status.HTTP_204_NO_CONTENT)
    


# @app.put("/posts/{id}", status_code=status.HTTP_200_OK)
# def update_post(id:int, post:Post):
#     post_id = str(id)
#     cursor.execute("UPDATE posts SET title=%s, content=%s, published=%s WHERE id=%s RETURNING *",
#                                             (post.title, post.content, post.published, post_id,))
#     updated_post = cursor.fetchone()
#     conn.commit()
#     if updated_post is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id:{id} not found")
#     return {"data": updated_post}

### using fastapi without routers
# from fastapi import FastAPI, Response, status, HTTPException, Depends
# from pydantic import BaseModel
# from typing import Optional, List
# from random import randrange
# import psycopg2
# from psycopg2.extras import RealDictCursor
# import time
# from sqlalchemy.orm import Session
# from . import models
# from . import schemas
# from .database import engine, get_db
# from .utils import hash

# @app.get("/posts", status_code=status.HTTP_200_OK, response_model=List[schemas.PostResponse])
# def get_posts(db: Session = Depends(get_db)):
#     posts = db.query(models.Post).all()
#     return posts

# @app.post('/posts', status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
# def create_post(post:schemas.PostCreate, db:Session = Depends(get_db)):
#     new_post = models.Post(**post.dict())
#     db.add(new_post)
#     db.commit()
#     db.refresh(new_post)
#     return new_post

# @app.get('/posts/{id}', status_code=status.HTTP_200_OK, response_model=schemas.PostResponse)
# def post_detail(id:int, db:Session = Depends(get_db)):
#     post = db.query(models.Post).filter(models.Post.id == id).first()
#     if post is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with id:{id} not found')
#     return post

# @app.put('/posts/{id}', status_code=status.HTTP_200_OK, response_model=schemas.PostResponse)
# def update_post(id:int, post_data:schemas.PostCreate, db:Session = Depends(get_db)):
#     post = db.query(models.Post).filter(models.Post.id == id)
#     if post.first() is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with id:{id} not found')
#     post.update(post_data.dict(), synchronize_session=False)
#     db.commit()
#     return post.first()

# @app.delete('/posts/{id}')
# def delete_post(id:int, db:Session = Depends(get_db)):
#     post = db.query(models.Post).filter(models.Post.id==id)
#     if post.first() is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with id:{id} not found')
#     post.delete(synchronize_session=False)
#     db.commit()
#     return Response(status_code=status.HTTP_204_NO_CONTENT)