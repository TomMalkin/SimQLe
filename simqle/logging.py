"""Contains the logger used by SimQLe."""
from loguru import logger as _logger

_logger.disable("simqle")

logger = _logger.bind(simqle=True)

RECOMMENDED_LOG_FORMAT = (
    "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green>"
    " | <level>{level: <8}</level>"
    " | <level>{message}</level>"
)


def simqle_filter(record):
    """Define the loguru filter for the SimQLe library."""
    return "simqle" in record["extra"]


def ignore_simqle_filter(record):
    """Define the loguru filter that ignores the SimQLe library."""
    return "simqle" not in record["extra"]
