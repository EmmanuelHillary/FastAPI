from fastapi import FastAPI
from . import models
from .database import engine
from .routers.posts import router as post_route
from .routers.users import router as user_route
from .routers.auth import router as auth_route
from .routers.likes import router as like_route
from fastapi.middleware.cors import CORSMiddleware
from .config import settings

# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(post_route)
app.include_router(user_route)
app.include_router(auth_route)
app.include_router(like_route)

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def index():
    return {"message": "Welcome to FastAPI - project by OceanHillz"}



