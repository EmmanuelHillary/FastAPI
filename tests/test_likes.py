import pytest
from app.models import Like


@pytest.fixture
def test_like(test_dummy_posts, session, test_dummy_user):
    new_like = Like(
        post_id=test_dummy_posts[3].id,
        user_id=test_dummy_user["id"]
    )
    session.add(new_like)
    session.commit()




def test_like_post(authorized_user, test_dummy_posts, test_dummy_user):
    post_id = test_dummy_posts[3].id
    res = authorized_user.post('/likes/', json={"post_id":test_dummy_posts[3].id})
    username = test_dummy_user["username"]
    assert res.status_code == 201
    assert res.json()["message"] == f'User:{username} liked post of id:{post_id}'

def test_unlike_post(authorized_user, test_dummy_posts, test_like):
    res = authorized_user.post('/likes/', json={"post_id":test_dummy_posts[3].id})
    assert res.status_code == 204

def test_like_unexistent_post(authorized_user, test_dummy_posts):
    res = authorized_user.post('/likes/', json={"post_id":9999})
    assert res.status_code == 404

def test_like_post_unauthorized(client, test_dummy_posts):
    res = client.post('/likes/', json={"post_id":test_dummy_posts[3].id})
    assert res.status_code == 401

