from utils.logger import setup_logger

logger = setup_logger()

class APIAssertions:

    def verify_status_code(self, response, expected_code):
        logger.info(f"Verifying status code: {expected_code}")
        assert response.status_code == expected_code

    def verify_key_value(self, response, key, expected_value):
        logger.info(f"Verifying response key: {key}")
        assert response.json()[key] == expected_value

    def verify_length(self, response, expected_length):
        logger.info("Verifying response length")
        assert len(response.json()) == expected_length