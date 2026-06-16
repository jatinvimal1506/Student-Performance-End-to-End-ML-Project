#Main aim of this is to read the dataset from some particular source- databases,files,cloud etc etc
import os 
import sys
from src.exception import CustomException
from src.logger import logging
import pandas as pd

from sklearn.model_selection import train_test_split
from dataclasses import dataclass

from src.components.data_transformation import DataTransformation #add to create the numpy arrays and store the preprecessed model 
from src.components.data_transformation import DataTransformationConfig 

from src.components.model_trainer import ModelTrainer
from src.components.model_trainer import ModelTrainerConfig

@dataclass
class DataIngestionConfig:
    train_data_path: str = os.path.join('artifacts', "train.csv")
    test_data_path: str = os.path.join('artifacts', "test.csv")
    raw_data_path: str = os.path.join('artifacts', "data.csv")

#main execution class
class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()

    def initiate_data_ingestion(self):
        #saving log message to show that data ingestin started
        logging.info("Entered the data ingestion method or component")

        try:
            df = pd.read_csv('notebook/stud.csv')

            logging.info('Read the dataset as dataframe')

            # Create the directory for train data if it does not exist
            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path),exist_ok=True)
            df.to_csv(self.ingestion_config.raw_data_path,index=False,header=True)

            # Log before splitting data
            logging.info("Train test split initiated")

            train_set, test_set = train_test_split(df,test_size=0.2,random_state=42)

            train_set.to_csv(self.ingestion_config.train_data_path,index=False,header=True) #write out column names - header
            test_set.to_csv(self.ingestion_config.test_data_path,index=False,header=True)

            # Log successful completion
            logging.info("Ingestion of the data is completed")

            # Return paths of train and test datasets
            return (
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path
            )

        except Exception as e:
            raise CustomException(e, sys)
        
#add artifacts in .gitignore
if __name__ == "__main__":
    # 1. Ingestion
    obj = DataIngestion()
    train_data_path, test_data_path = obj.initiate_data_ingestion()

    data_transformation = DataTransformation()
    train_arr, test_arr, _ = data_transformation.initiate_data_transformation(train_data_path, test_data_path)

    model_trainer = ModelTrainer()
    r2_score_result = model_trainer.initiate_model_trainer(train_arr, test_arr)
    print(f"Best Model R2 Score: {r2_score_result}")