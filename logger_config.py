# logger_config.py

import os
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime, timedelta


# Ensure logs directory exists
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)


# Delete log files older than 7 days
def delete_old_logs(directory, days=7):
    now = datetime.now()
    cutoff = now - timedelta(days=days)

    for filename in os.listdir(directory):
        if filename.endswith(".log"):
            file_path = os.path.join(directory, filename)
            if os.path.isfile(file_path):
                file_mtime = datetime.fromtimestamp(os.path.getmtime(file_path))
                if file_mtime < cutoff:
                    os.remove(file_path)
                    print(f"Deleted old log: {file_path}")

delete_old_logs(LOG_DIR)

# Define log file path
LOG_FILE_PATH = os.path.join(LOG_DIR, "app.log")

# Create rotating file handler
file_handler = RotatingFileHandler(
    LOG_FILE_PATH, maxBytes=10**6, backupCount=5
)
file_handler.setFormatter(logging.Formatter(
    "%(asctime)s [%(levelname)s] [%(name)s] %(message)s"
))

# Create and configure logger
logger = logging.getLogger("whatsapp_api")
logger.setLevel(logging.INFO)
logger.addHandler(file_handler)

# Also log to console
console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter(
    "%(asctime)s [%(levelname)s] [%(name)s] %(message)s"
))
logger.addHandler(console_handler)
