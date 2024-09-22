# This file contains the custom exception class which will be raised when any error occurs in the code.

import sys
from src.logging import logger 

class NetworkSecurityException(Exception): # Custom exception class
    def __init__(self,error_message,error_details:sys):
        self.error_message = error_message # We are storing the error message in the object
        _,_,exc_tb = error_details.exc_info() # We are extracting the line number and file name where the error occured, exc_tb is the traceback
        
        self.lineno=exc_tb.tb_lineno # Extracting the line number
        self.file_name=exc_tb.tb_frame.f_code.co_filename  # Extracting the file name
    
    def __str__(self): # This function will be called when we print the object of this class
        return "Error occured in python script name [{0}] line number [{1}] error message [{2}]".format(
        self.file_name, self.lineno, str(self.error_message)) # This function will be called when we print the object of this class
        
if __name__=='__main__':
    try:
        logger.logging.info("Enter the try block")
        a=1/0
        print("This will not be printed",a)
    except Exception as e:
           raise NetworkSecurityException(e,sys)