import logging

def setup_logger():
    logger = logging.getLogger("API_Automation")
    logger.setLevel(logging.INFO)

    handler = logging.FileHandler("api_logs.log")
    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(message)s"
    )

    handler.setFormatter(formatter)

    if not logger.handlers:
        logger.addHandler(handler)

    return logger