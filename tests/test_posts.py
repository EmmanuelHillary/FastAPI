from app.schemas import PostDetail, PostResponse
import pytest

def test_get_posts(authorized_user, test_dummy_posts):
    res = authorized_user.get('/posts/')
    def get_post(post):
        return PostDetail(**post)
    post_map = map(get_post, res.json())
    posts = list(post_map)
    assert posts[0].Post.title == res.json()[0]["Post"]["title"]
    assert posts[1].Post.title == res.json()[1]["Post"]["title"]
    assert posts[2].Post.title == res.json()[2]["Post"]["title"]
    assert res.status_code == 200
    assert len(res.json()) == len(test_dummy_posts)

def test_get_posts_unauthorized(client, test_dummy_posts):
    res = client.get('/posts/')
    assert res.status_code == 401

def test_get_post_unauthorized(client, test_dummy_posts):
    res = client.get(f'/posts/{test_dummy_posts[0].id}')
    assert res.status_code == 401

def test_get_unexistent_post(authorized_user, test_dummy_posts):
    res = authorized_user.get(f'/posts/999999')
    assert res.status_code == 404

def test_get_post(authorized_user, test_dummy_posts):
    res = authorized_user.get(f'/posts/{test_dummy_posts[0].id}')
    post = PostDetail(**res.json())
    assert res.status_code == 200
    assert post.Post.title == test_dummy_posts[0].title
    assert post.Post.content == test_dummy_posts[0].content
    assert post.Post.published == test_dummy_posts[0].published

@pytest.mark.parametrize("title, content, published",[
    ("awesome new title", "awesome new content", True),
    ("Favourite pizza", "i love pepperoni", False),
    ("tallest skyscraper", "wahoo", True)
])
def test_create_post(authorized_user, test_dummy_user, title, content, published):
    res = authorized_user.post(f'/posts/', json={"title": title, "content": content, "published": published})
    post = PostResponse(**res.json())
    assert res.status_code == 201
    assert post.title == title
    assert post.content == content
    assert post.published == published
    assert post.user.id == test_dummy_user['id']

def test_create_post_default_published(authorized_user, test_dummy_user,):
    res = authorized_user.post(f'/posts/', json={"title": "title", "content": "content"})
    post = PostResponse(**res.json())
    assert res.status_code == 201
    assert post.title == "title"
    assert post.content == "content"
    assert post.published == False
    assert post.user.id == test_dummy_user['id']

def test_create_post_unauthorised(client):
    res = client.post(f'/posts/', json={"title": "title", "content": "content"})
    assert res.status_code == 401

def test_delete_post(authorized_user, test_dummy_posts):
    res = authorized_user.delete(f'/posts/{test_dummy_posts[0].id}')
    assert res.status_code == 204

def test_delete_post_unauthorized(client, test_dummy_posts):
    res = client.delete(f'/posts/{test_dummy_posts[0].id}')
    assert res.status_code == 401

def test_delete_unexistent_post(authorized_user, test_dummy_posts):
    res = authorized_user.delete(f'/posts/9999999')
    assert res.status_code == 404

def test_delete_another_users_post(authorized_user, test_dummy_posts):
    res = authorized_user.delete(f'/posts/{test_dummy_posts[3].id}')
    assert res.status_code == 403

def test_post_update(authorized_user, test_dummy_posts):
    data={
            'title': "Update Post",
            'content': "Update Content",
            "published": True
        }
    res = authorized_user.put(f'/posts/{test_dummy_posts[0].id}', json=data)
    post = PostResponse(**res.json())
    assert res.status_code == 200
    assert post.title == data["title"]
    assert post.content == data["content"]
    assert post.published == data["published"]

def test_post_update_unauthorised(client, test_dummy_posts):
    data={
            'title': "Update Post",
            'content': "Update Content",
            "published": True
        }
    res = client.put(f'/posts/{test_dummy_posts[0].id}', json=data)
    assert res.status_code == 401

def test_update_unexistent_post(authorized_user, test_dummy_posts):
    data={
            'title': "Update Post",
            'content': "Update Content",
            "published": True
        }
    res = authorized_user.put(f'/posts/9999999', json=data)
    assert res.status_code == 404

def test_update_another_user_post(authorized_user, test_dummy_posts):
    data={
            'title': "Update Post",
            'content': "Update Content",
            "published": True
        }
    res = res = authorized_user.put(f'/posts/{test_dummy_posts[3].id}', json=data)
    assert res.status_code == 403


