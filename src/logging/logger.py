# Desc: Logging configuration for the application

# Importing required modules
import logging
import os
from datetime import datetime

# Creating a log file with the current timestamp
LOG_FILE=f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log" # Log file name with the current timestamp

logs_path=os.path.join(os.getcwd(),"logs",LOG_FILE) # Path to the logs folder
os.makedirs(logs_path,exist_ok=True) # Creating the logs folder if it doesn't exist

LOG_FILE_PATH=os.path.join(logs_path,LOG_FILE) # Path to the log file

logging.basicConfig(
    filename=LOG_FILE_PATH,
    format="[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s", # Format of the log message
    level=logging.INFO,
)