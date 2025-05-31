import logging

logger = logging.getLogger("notification_logger")
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler("notifications.log")
file_handler.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

if not logger.hasHandlers():
    logger.addHandler(file_handler)
