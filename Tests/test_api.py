import json
import pytest
from Services.services_api import APIService
from utils.assertions import APIAssertions

service = APIService()
assertions = APIAssertions()

# Load JSON data
with open("data/test_data.json") as f:
    test_data = json.load(f)

# TC001 – Get all posts
def test_get_posts(session):
    response = service.get_posts(session)
    assertions.verify_status_code(response, 200)
    assertions.verify_length(response, 100)

# TC002 – Get post by id (1,5,10)
@pytest.mark.parametrize("post_id", [1, 5, 10])
def test_get_post_by_id(session, post_id):
    response = service.get_post_by_id(session, post_id)
    assertions.verify_status_code(response, 200)
    assertions.verify_key_value(response, "id", post_id)

# TC003 – Create post
@pytest.mark.parametrize("data", test_data["create_post"])
def test_create_post(session, data):
    response = service.create_post(session, data)
    assertions.verify_status_code(response, 201)
    assertions.verify_key_value(response, "title", data["title"])

# TC004 – Update post
def test_update_post(session):
    update_data = test_data["update_post"]
    response = service.update_post(session, 1, update_data)
    assertions.verify_status_code(response, 200)
    assertions.verify_key_value(response, "title", update_data["title"])

# TC005 – Delete post
def test_delete_post(session):
    response = service.delete_post(session, 1)
    assertions.verify_status_code(response, 200)

# TC006 – Get non-existent post
def test_get_non_existent_post(session):
    response = service.get_post_by_id(session, 9999)
    assertions.verify_status_code(response, 404)

# TC007 – Create post with invalid data
def test_create_post_invalid_data(session):
    invalid_data = {"invalid": "data"}
    response = service.create_post(session, invalid_data)
    assertions.verify_status_code(response, 201)

# TC008 – Get all users
def test_get_users(session):
    response = service.get_users(session)
    assertions.verify_status_code(response, 200)
    assertions.verify_length(response, 10)

# TC009 – Get all comments
def test_get_comments(session):
    response = service.get_comments(session)
    assertions.verify_status_code(response, 200)
    assertions.verify_length(response, 500)

# TC010 – Get post comments
def test_get_post_comments(session):
    response = session.get("https://jsonplaceholder.typicode.com/posts/1/comments")
    assertions.verify_status_code(response, 200)
    assert len(response.json()) > 0