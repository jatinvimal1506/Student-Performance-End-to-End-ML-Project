from src.exception import CustomException
import os
import sys

import dill
import pickle


def save_object(file_path, obj): #save the model in the given directory given from the data_transformation
    try:
        dir_path = os.path.dirname(file_path) #get the directory
        os.makedirs(dir_path, exist_ok=True) #make the directory

        with open(file_path, "wb") as file_obj: #dump the pickle file in the file path along with the object 
            pickle.dump(obj, file_obj) #data serialse so we open in write binary and then dump 

    except Exception as e:
        raise CustomException(e, sys)
    
def load_object(file_path):
    try:
        with open(file_path, "rb") as file_obj: #same thing insated of write we do read return the pkl file stored in the path
            return pickle.load(file_obj)

    except Exception as e:
        raise CustomException(e, sys)
