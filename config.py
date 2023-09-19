import configparser
import os

# get current working directory
working_directory = os.getcwd()

# parses config.ini file that is in same directory
configParser = configparser.RawConfigParser()
configFilePath = f'{working_directory}/config.ini'
parser = configparser.ConfigParser()

if os.path.exists(configFilePath) is False:
    raise Exception(f'{configFilePath} not found')

# try to open config file
try:
    parser.read(configFilePath)
except Exception as e:
    e

# get funderbeam config values
funderbeam_username = parser.get('Funderbeam', 'username')
funderbeam_password = parser.get('Funderbeam', 'password')
