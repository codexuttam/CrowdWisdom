import logging
import os
from datetime import datetime

# Configure logging
LOG_DIR = "/home/codebloodedsash/CrowdWisdom/logs"
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

log_file = os.path.join(LOG_DIR, f"trading_agent_{datetime.now().strftime('%Y%m%d')}.log")

# Create logger
logger = logging.getLogger("CrowdWisdom")
logger.setLevel(logging.INFO)

# File handler
file_handler = logging.FileHandler(log_file)
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))

# Console handler
console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter('%(levelname)s: %(message)s'))

logger.addHandler(file_handler)
logger.addHandler(console_handler)

def get_logger():
    return logger
