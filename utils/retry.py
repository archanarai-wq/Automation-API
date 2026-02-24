import requests
import time
from utils.logger import setup_logger

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