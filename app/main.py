# Run with "uv run fastapi dev main.py"
from app.utils.config import config
from app.api import app
import logging

logging.basicConfig(
    level=logging.INFO
)