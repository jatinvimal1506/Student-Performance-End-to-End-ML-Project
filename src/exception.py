import sys #built in library - used to interct with system specific parameter , functions , variables - interact with python intrepreter and run time envirnoment
from src.logger import logging #log your custom error as well

#Function to return the custom error message 
def error_message_detail(error,error_detail:sys):
    _,_,exe_tb = error_detail.exc_info() #exe_tb is the traceback object - goes to entire history where your code travelled befoe it crashed 

    file_name = exe_tb.tb_frame.f_code.co_filename
    error_message = "Error occured in Pyhton Script [{0}] line number [{1}] error message [{2}]".format(file_name,exe_tb.tb_lineno,str(error))

    return error_message

#Creating a class to create a custom error message that will give us the exception with the message generated(returned by function)
class CustomException(Exception): #Inherit from inbuilt Exception class
    def __init__(self,error_message,error_detail:sys):
        super().__init__(error_message) #call __init__ func of parent class
        self.error_message = error_message_detail(error_message,error_detail=error_detail)

    def __str__(self): #initaised as soon as print function is called om object
        return self.error_message    