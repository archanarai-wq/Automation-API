import pytest
import requests
import time

BASE_URL = "https://jsonplaceholder.typicode.com"


#retry decorator
def retry(func):
    def wrapper(*args, **kwargs):
        attempts = 0
        while attempts < 3:
            try:
                return func(*args, **kwargs)
            except requests.exceptions.RequestException as e:
                attempts += 1
                print(f"Retry {attempts} due to error: {e}")
                time.sleep(2)
        raise Exception("Max retries exceeded")
    return wrapper

@pytest.fixture
def session():
    s = requests.Session()
    yield s
    s.close()

@retry
def get_posts(session):
    response = session.get(f"{BASE_URL}/posts")
    return response

def generate_post_data():
    yield {"title": "foo", "body": "bar", "userId": 1}
    yield {"title": "baz", "body": "qux", "userId": 2}

@retry
def get_post_by_id(session, post_id):
    response = session.get(f"{BASE_URL}/posts/{post_id}")
    return response


@retry
def update_post(session, post_id, data):
    response = session.put(f"{BASE_URL}/posts/{post_id}", json=data)
    return response


@retry
def delete_post(session, post_id):
    response = session.delete(f"{BASE_URL}/posts/{post_id}")
    return response


@retry
def get_users(session):
    response = session.get(f"{BASE_URL}/users")
    return response


@retry
def get_comments(session):
    response = session.get(f"{BASE_URL}/comments")
    return response

#TC001:- Get all posts
def test_get_posts(session):
    response = get_posts(session)
    assert response.status_code == 200
    assert len(response.json()) == 100

#TC002:- Get posts by ids 1,5,10
@pytest.mark.parametrize("post_id", [1, 5, 10])
def test_get_post_by_id(session, post_id):
    response = get_post_by_id(session, post_id)
    assert response.status_code == 200
    assert response.json()["id"] == post_id

#TC003:- Create new post
@pytest.mark.parametrize("data", generate_post_data())
def test_create_post(session, data):
    response = session.post(f"{BASE_URL}/posts", json=data)
    assert response.status_code == 201
    assert response.json()["title"] == data["title"]

#TC004:- Update existing post
def test_update_post(session):
    update_data = {
        "title": "updated title",
        "body": "updated body",
        "userId": 1
    }
    response = update_post(session, 1, update_data)
    assert response.status_code == 200
    assert response.json()["title"] == "updated title"

#TC005:-Delete post
def test_delete_post(session):
    response = delete_post(session, 1)
    assert response.status_code == 200

#TC006:- Get non-existent post
def test_get_non_existent_post(session):
    response = session.get(f"{BASE_URL}/posts/9999")
    assert response.status_code == 404

#TC007:- Create post with invalid data
def test_create_post_invalid_data(session):
    invalid_data = {"invalid": "data"}
    response = session.post(f"{BASE_URL}/posts", json=invalid_data)
    assert response.status_code == 201

#TC008:- Get all users
def test_get_users(session):
    response = get_users(session)
    assert response.status_code == 200
    assert len(response.json()) == 10

#TC009:- Get all comments
def test_get_comments(session):
    response = get_comments(session)
    assert response.status_code == 200
    assert len(response.json()) == 500

#TC0010:- Get post comments
def test_get_post_comments(session):
    response = session.get(f"{BASE_URL}/posts/1/comments")
    assert response.status_code == 200
    assert len(response.json()) > 0





