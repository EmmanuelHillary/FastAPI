from app.schemas import UserResponse, Token
from app.config import settings
from jose import jwt
import pytest
    


def test_create_user(client):
    res = client.post('/users/', json={"username":"TheHillz", "email":"TheHillz@mail.com", "password": "Password123"})
    response = UserResponse(**res.json())
    assert res.status_code == 201
    assert response.username == 'TheHillz'
    assert response.email == 'TheHillz@mail.com'

def test_login(client, test_dummy_user):
    res = client.post('/login', data={'username': test_dummy_user['username'], 'password': test_dummy_user['password']})
    token = Token(**res.json())
    payload = jwt.decode(token.access_token, settings.secret_key, algorithms=[settings.algorithm])
    user_username = payload.get("user_username")
    user_id= payload.get("user_id")
    assert res.status_code == 200
    assert test_dummy_user['id'] == user_id
    assert test_dummy_user['username'] == user_username

@pytest.mark.parametrize("username, password, status", [
    ('TheHillz', 'Password123', 200),
    ('TheHillz', 'Password12', 403),
    ('TheHill', 'Password123', 403),
    (None, 'Password123', 422),
    ('TheHillz', None, 422),
])
def test_incorrect_login(client, test_dummy_user, username, password, status):
    res = client.post('/login', data={'username': username, 'password': password})

    assert res.status_code == status
    



