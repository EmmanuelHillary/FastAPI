from fastapi.testclient import TestClient
from app.main import app
import pytest
from app.database import get_db, Base
from sqlalchemy import create_engine
from app.schemas import UserResponse
from sqlalchemy.orm import sessionmaker
from app.Oauth2 import create_access_token
from app.models import Post

TEST_DATABASE_URL = 'postgresql://postgres:Nintendo1.@localhost:5432/test_db'
engine = create_engine(TEST_DATABASE_URL)

TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    try:
        db = TestSessionLocal()
        yield db
    finally:
        db.close()
    

@pytest.fixture
def client(session):
    def override_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_db
    yield TestClient(app)

@pytest.fixture
def test_dummy_user(client):
    user_data = {"username":"TheHillz", "email":"TheHillz@mail.com", "password": "Password123"}
    res = client.post('/users/',json=user_data)
    user = res.json()
    user["password"] = user_data["password"]
    response = UserResponse(**res.json())
    assert res.status_code == 201
    assert response.username == 'TheHillz'
    assert response.email == 'TheHillz@mail.com'
    return user

@pytest.fixture
def test_dummy_user2(client):
    user_data = {"username":"TheHillz1", "email":"TheHillz1@mail.com", "password": "Password123"}
    res = client.post('/users/',json=user_data)
    user = res.json()
    user["password"] = user_data["password"]
    response = UserResponse(**res.json())
    assert res.status_code == 201
    assert response.username == 'TheHillz1'
    assert response.email == 'TheHillz1@mail.com'
    return user

@pytest.fixture
def dummy_token(test_dummy_user):
    token = create_access_token(data={"user_id":test_dummy_user['id'], "user_username": test_dummy_user['username']})
    return token

@pytest.fixture
def authorized_user(client, dummy_token):
    client.headers = {
        **client.headers,
        "Authorization": f'Bearer {dummy_token}'
    }
    return client

@pytest.fixture
def test_dummy_posts(test_dummy_user, test_dummy_user2, session):
    post_data = [
        {
            'title': "First Post",
            'content': "First Content",
            'user_id': test_dummy_user['id']
        },
        {
            'title': "Second Post",
            'content': "Second Content",
            'user_id': test_dummy_user['id']
        },
        {
            'title': "Third Post",
            'content': "Third Content",
            'user_id': test_dummy_user['id']
        },
        {
            'title': "Fourth Post",
            'content': "Fourth Content",
            'user_id': test_dummy_user2['id']
        },
    ]

    def create_post(post):
        return Post(**post)
    
    post_map = map(create_post, post_data)
    posts = list(post_map)
    session.add_all(posts)
    session.commit()
    posts = session.query(Post).all()
    return posts