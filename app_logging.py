from loguru import logger
import sys
import traceback
from types import TracebackType
from typing import Optional, Type

LOGGER_LEVEL = "DEBUG"


def setup_loguru_logger() -> None:
    logger.remove()
    log_format = (
        "<green>{time:YYYY-MM-DD HH:mm:ss.SSS ZZ}</green> | <level>{level: <8}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>{exception}"
    )
    logger.add(sys.stderr, level=LOGGER_LEVEL, format=log_format, colorize=True, backtrace=True, diagnose=True)


def handle_exception(
    exc_type: Type[BaseException],
    exc_value: BaseException,
    exc_traceback: Optional[TracebackType],
) -> None:
    """Global exception handler to catch and log any uncaught exceptions:"""
    # Allow program to exit without logging an error when KeyboardInterrupt is raised
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
    else:
        traceback_string = "".join(traceback.format_exception(exc_type, exc_value, exc_traceback))
        logger.error(
            f"An unhandled exception occurred: {exc_type.__name__}: {exc_value}, traceback: {traceback_string}"
        )


sys.excepthook = handle_exception
setup_loguru_logger()