#logger.py is used to track all the logs of the project - like what all happens in the project 

import logging  #built in library - track all errors,events and warning
import os  #built in libraray - interact with os - files 
from datetime import datetime

LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log" #create a filename based on current time this is the format (e.g., 06_14_2026_12_55_30.log)

# Create a directory path for where logs should be stored
# os.getcwd() gets your Current Working Directory (the root folder of your project) and .join(os.getcwd(),"logs",LOG_FILE) will give the path where to make the log filr
# This joins your project folder with a new sub-folder named "logs" and adds our timestamped filename
logs_path = os.path.join(os.getcwd(), "logs", LOG_FILE)

#create the given directory using the path 
os.makedirs(logs_path, exist_ok=True)

#make the fianl path of the log file
LOG_FILE_PATH = os.path.join(logs_path, LOG_FILE)

logging.basicConfig(
    filename=LOG_FILE_PATH,  #gives the path whwre to write the logs and if no path given will print in the terminal
    
    # how each line of the log file will look like the structure
    # [%(asctime)s]   -> Automatically records the exact timestamp of the log event
    # %(lineno)d      -> Logs the exact line number of the code where the message came from
    # %(name)s        -> Logs the module name (e.g., __main__ or root)
    # %(levelname)s   -> Logs the severity level (e.g., INFO, WARNING, ERROR)
    # %(message)s     -> The custom message text you write
    format="[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    
    # Sets the minimum threshold level. INFO means it will capture everything except low-level DEBUG logs 
    level=logging.INFO
) 
#what does configuration mean - basically sepearting the settings and the actual logic to make the life easier and easy to maintain