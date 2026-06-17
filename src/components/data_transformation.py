import os
import sys #to interatc with runtime envirnoment - use in custom error
import numpy as np 
import pandas as pd
from dataclasses import dataclass #no need of__init__

from sklearn.compose import ColumnTransformer #combine steps for multiple coulmn
from sklearn.preprocessing import OneHotEncoder,StandardScaler
from sklearn.impute import SimpleImputer #handle missing values mediain for numerical and mode for categorical
from sklearn.pipeline import Pipeline #combine steps in a single column 

from src.logger import logging
from src.exception import CustomException

from src.utils import save_object

@dataclass
class DataTransformationConfig: #to store the input(where to store the ouput or the preprocessed model)
    preprocessor_obj_file_path: str=os.path.join('artifacts',"preprocessor.pkl") #make the path using os.join artifacts/preprocessor.pkl

class DataTransformation:
    def __init__(self):
        self.data_transformation_config=DataTransformationConfig() 

    def get_data_transformer_object(self): #main function responsible for data transformation 
        try:
            numerical_columns = ["writing_score", "reading_score"]
            categorical_columns = [
                "gender",
                "race_ethnicity",
                "parental_level_of_education",
                "lunch",
                "test_preparation_course",
            ]

            num_pipeline= Pipeline( #perform imputation + scalung of the numerical features ising the pipeline 
                steps=[
                ("imputer",SimpleImputer(strategy="median")),
                ("scaler",StandardScaler())

                ]
            )

            cat_pipeline=Pipeline( #perform imputation(mode) + OHE encoding + scaling of the categorical features ising the pipeline 

                steps=[
                ("imputer",SimpleImputer(strategy="most_frequent")),
                ("one_hot_encoder",OneHotEncoder()),
                ("scaler",StandardScaler(with_mean=False))
                ]

            )

            logging.info(f"Categorical columns: {categorical_columns}")
            logging.info(f"Numerical columns: {numerical_columns}")

            preprocessor=ColumnTransformer( #now do both transfromaton for numerical columns and catrgorical features
                [
                ("num_pipeline",num_pipeline,numerical_columns),
                ("cat_pipelines",cat_pipeline,categorical_columns)
                ]

            )

            return preprocessor #return the model 
        
        except Exception as e:
            raise CustomException(e,sys)
        
    def initiate_data_transformation(self,train_path,test_path):
        try:
            train_df=pd.read_csv(train_path) #already saved in artifacts from the data ingestion.py
            test_df=pd.read_csv(test_path)

            logging.info("Read train and test data completed")

            logging.info("Obtaining preprocessing object")

            preprocessing_obj=self.get_data_transformer_object()

            target_column_name="math_score"
            numerical_columns = ["writing_score", "reading_score"]

            input_feature_train_df=train_df.drop(columns=[target_column_name],axis=1) #basically X_train
            target_feature_train_df=train_df[target_column_name] #y_train

            input_feature_test_df=test_df.drop(columns=[target_column_name],axis=1) #basically X_test
            target_feature_test_df=test_df[target_column_name] #basically y_test

            logging.info(f"Applying preprocessing object on training dataframe and testing dataframe.")

            input_feature_train_arr=preprocessing_obj.fit_transform(input_feature_train_df) #Apply the fit_transform on train and transform on test to prevent data lekage
            input_feature_test_arr=preprocessing_obj.transform(input_feature_test_df) 

            #main aim is to convet the train_dat and test_data into np array for fast calcualtions
            train_arr = np.c_[input_feature_train_arr, np.array(target_feature_train_df)] #np.c_ means column wise concatenation 
            test_arr = np.c_[input_feature_test_arr, np.array(target_feature_test_df)]

            logging.info(f"Saved preprocessing object.")

            save_object(
                file_path=self.data_transformation_config.preprocessor_obj_file_path,
                obj=preprocessing_obj
            )

            return (
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_obj_file_path,
            )
        except Exception as e:
            raise CustomException(e,sys)
