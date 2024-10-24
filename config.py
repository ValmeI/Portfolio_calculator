import configparser
import os

# get current working directory
working_directory = os.getcwd()

# parses config.ini file that is in same directory
configParser = configparser.RawConfigParser()
configFilePath = f"{working_directory}/config.ini"
parser = configparser.ConfigParser()

if os.path.exists(configFilePath) is False:
    raise Exception(f"{configFilePath} not found")

# try to open config file
try:
    parser.read(configFilePath)
except Exception as e:
    raise e

# get funderbeam config values
FUNDERBEAM_USERNAME = parser.get("Funderbeam", "username")
FUNDERBEAM_PASSWORD = parser.get("Funderbeam", "password")
LOGGER_LEVEL = parser.get("LOGGER", "level")
TWILIO_APY_KEY = parser.get("TWILIO", "api_key")
FINNHUB_API_KEY = parser.get("FINNHUB", "api_key")
