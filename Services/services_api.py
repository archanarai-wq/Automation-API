import requests
from utils.logger import setup_logger
from utils.retry import retry

logger = setup_logger()
BASE_URL = "https://jsonplaceholder.typicode.com"

class APIService:
    @retry
    def get_posts(self, session):
        response = session.get(f"{BASE_URL}/posts")
        return response

    @retry
    def get_post_by_id(self, session, post_id):
        response = session.get(f"{BASE_URL}/posts/{post_id}")
        return response

    @retry
    def create_post(self, session, data):
        logger.info("Creating new post")
        return session.post(f"{BASE_URL}/posts", json=data)

    @retry
    def update_post(self, session, post_id, data):
        response = session.put(f"{BASE_URL}/posts/{post_id}", json=data)
        return response

    @retry
    def delete_post(self, session, post_id):
        response = session.delete(f"{BASE_URL}/posts/{post_id}")
        return response

    @retry
    def get_users(self, session):
        response = session.get(f"{BASE_URL}/users")
        return response

    @retry
    def get_comments(self, session):
        response = session.get(f"{BASE_URL}/comments")
        return response
