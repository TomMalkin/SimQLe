"""Contains the logger used by SimQLe."""
from loguru import logger

logger.disable("simqle")

RECOMMENDED_LOG_FORMAT = (
    "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green>"
    " | <level>{level: <8}</level>"
    " | <level>{message}</level>"
)
