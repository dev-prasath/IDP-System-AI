# =========================================================
# IMPORTS
# =========================================================

import logging
import os
from logging.handlers import RotatingFileHandler

# =========================================================
# LOG DIRECTORY SETUP
# =========================================================

LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "system.log")

os.makedirs(LOG_DIR, exist_ok=True)

# =========================================================
# LOGGER CONFIGURATION
# =========================================================

logger = logging.getLogger("IDP_SYSTEM")
logger.setLevel(logging.INFO)

# Prevent duplicate logs
logger.propagate = False

# =========================================================
# FORMATTER
# =========================================================

formatter = logging.Formatter(
    "%(asctime)s | %(levelname)s | %(filename)s | "
    "%(funcName)s | Line:%(lineno)d | %(message)s"
)

# =========================================================
# FILE HANDLER
# =========================================================

file_handler = RotatingFileHandler(
    LOG_FILE,
    maxBytes=5 * 1024 * 1024,
    backupCount=5,
    encoding="utf-8"
)

file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)

# =========================================================
# CONSOLE HANDLER
# =========================================================

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)

# =========================================================
# ATTACH HANDLERS
# =========================================================

if not logger.handlers:
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

# =========================================================
# HELPER FUNCTIONS
# =========================================================


def log_info(message: str):
    logger.info(message)



def log_warning(message: str):
    logger.warning(message)



def log_error(message: str):
    logger.error(message)



def log_exception(message: str):
    logger.exception(message)