# Description: This file contains the code to ingest data from the database and export it to the feature store.

## Importing Required Libraries
import os
import sys
import numpy as np
import pandas as pd
import pymongo
from typing import List
from sklearn.model_selection import train_test_split
from dotenv import load_dotenv
from src.exception.exception import NetworkSecurityException
from src.logging.logger import logging
from src.entity.config_entity import DataIngestionConfig, MLOpsPipelineConfig
from src.entity.artifact_entity import DataIngestionArtifact

## Data Ingestion Class
class DataIngestion:
    def __init__(self,data_ingestion_config:DataIngestionConfig, mongo_db_url):
        try:
            self.data_ingestion_config=data_ingestion_config
            self.mongo_db_url=mongo_db_url
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def export_collection_as_dataframe(self) -> pd.DataFrame:
        """
        Read data from mongodb
        """
        try:
            database_name=self.data_ingestion_config.database_name
            collection_name=self.data_ingestion_config.collection_name
            self.mongo_client=pymongo.MongoClient(self.mongo_db_url)
            collection=self.mongo_client[database_name][collection_name]

            df=pd.DataFrame(list(collection.find())) ## convert the collection to dataframe

            if "_id" in df.columns.to_list(): ## remove the _id column
                df=df.drop(columns=["_id"],axis=1)
            
            df.replace({"na":np.nan},inplace=True) ## replace na with np.nan
            logging.info(f"Exported collection {collection_name} from {database_name} database as dataframe")
            return df
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def export_data_into_feature_store(self,dataframe: pd.DataFrame):
        try:
            feature_store_file_path=self.data_ingestion_config.feature_store_file_path
            #creating folder
            dir_path = os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path,exist_ok=True)
            dataframe.to_csv(feature_store_file_path,index=False,header=True)
            logging.info(f"Exported dataframe to feature store file path {feature_store_file_path}")
            return dataframe
            
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def split_data_as_train_test(self,dataframe: pd.DataFrame):
        try:
            train_set, test_set = train_test_split(dataframe, test_size=self.data_ingestion_config.train_test_split_ratio)
           
            logging.info("Performed train test split on the dataframe")
            logging.info("Exited split_data_as_train_test method of Data_Ingestion class")
            
            ## creating folder for train file
            dir_training_path = os.path.dirname(self.data_ingestion_config.training_file_path)
            os.makedirs(dir_training_path, exist_ok=True)

            # creating folder for train file
            dir_testing_path = os.path.dirname(self.data_ingestion_config.training_file_path)
            os.makedirs(dir_testing_path, exist_ok=True)
            
            logging.info(f"Exporting train and test file path.")
            
            # Exporting the train and test file
            train_set.to_csv(self.data_ingestion_config.training_file_path, index=False, header=True)
            test_set.to_csv(self.data_ingestion_config.testing_file_path, index=False, header=True)
            
            logging.info(f"Exported train and test file.")
            
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
        
    def initiate_data_ingestion(self) -> DataIngestionArtifact:
        try:
            # Exporting the collection as dataframe
            
            dataframe=self.export_collection_as_dataframe()
            dataframe=self.export_data_into_feature_store(dataframe)
            self.split_data_as_train_test(dataframe)
            dataingestionartifact=DataIngestionArtifact(trained_file_path=self.data_ingestion_config.training_file_path,test_file_path=self.data_ingestion_config.testing_file_path)
            logging.info("Data ingested to the feature store and split into train and test set")
            return dataingestionartifact

        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
if __name__=="__main__":
    pass
   
