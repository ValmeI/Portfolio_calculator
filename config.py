from pydantic_settings import BaseSettings
from typing import Literal


class Settings(BaseSettings):

    funderbeam_username: str
    funderbeam_password: str

    # Valid log levels that loguru accepts, incase there is typos in the .env and it would make whole code unresponsive
    logger_level: Literal["TRACE", "DEBUG", "INFO", "SUCCESS", "WARNING", "ERROR", "CRITICAL"]

    twilio_api_key: str
    finnhub_api_key: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


try:
    settings = Settings()
except Exception as e:
    raise ValueError(f"Environment validation failed: {str(e)}") from e

# Assign to global variables (optional, for backward compatibility)
FUNDERBEAM_USERNAME = settings.funderbeam_username
FUNDERBEAM_PASSWORD = settings.funderbeam_password
LOGGER_LEVEL = settings.logger_level
TWILIO_API_KEY = settings.twilio_api_key
FINNHUB_API_KEY = settings.finnhub_api_key
