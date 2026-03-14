import logging
import sys
from pathlib import Path

# Create logs directory
LOGS_DIR = Path("logs")
LOGS_DIR.mkdir(exist_ok=True)

def setup_logging():
    error_handler = logging.FileHandler(LOGS_DIR / "error.log")
    error_handler.setLevel(logging.ERROR)
    
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler(LOGS_DIR / "app.log"),
            error_handler,
            logging.FileHandler(LOGS_DIR / "auth.log"),
        ]
    )
    
    # Auth specific logger
    auth_logger = logging.getLogger("auth")
    auth_handler = logging.FileHandler(LOGS_DIR / "auth.log")
    auth_handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
    auth_logger.addHandler(auth_handler)
    auth_logger.propagate = False

setup_logging()
logger = logging.getLogger("app")
auth_logger = logging.getLogger("auth")
