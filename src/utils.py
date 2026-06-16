from src.exception import CustomException
import os
import sys

import dill
import pickle

from sklearn.metrics import r2_score
from sklearn.model_selection import GridSearchCV



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

def evaluate_models(X_train, y_train, X_test, y_test, models, param):
    try:
        report = {} #keep track of the model reports 
        trained_models = {} #save the trained models 

        for i in range(len(list(models))):
            model_name = list(models.keys())[i]
            model = list(models.values())[i]
            para = param[model_name]

            #Initialize instance and run hyperparameter tuning via GridSearchCV
            gs = GridSearchCV(model, para, cv=3)
            gs.fit(X_train, y_train)

            #get best estimator using the onject created
            best_tuned_model = gs.best_estimator_

            #get y_pred 
            y_train_pred = best_tuned_model.predict(X_train)
            y_test_pred = best_tuned_model.predict(X_test)

            #calculate score 
            train_model_score = r2_score(y_train, y_train_pred)
            test_model_score = r2_score(y_test, y_test_pred)

            #assing the model with the test_score 
            report[model_name] = test_model_score
            trained_models[model_name] = best_tuned_model

        return report,trained_models

    except Exception as e:
        raise CustomException(e, sys)