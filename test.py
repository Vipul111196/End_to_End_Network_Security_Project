import os
import sys
from src.logging.logger import logging 
from src.exception.exception import NetworkSecurityException
from src.entity.config_entity import MLOpsPipelineConfig, DataIngestionConfig
from src.entity.artifact_entity import DataIngestionArtifact
from src.components.data_ingestion import DataIngestion
from dotenv import load_dotenv

# Loading the environment variables
load_dotenv()

if __name__ == "__main__":
    try:
        # Data Ingestion Process
        mongo_db_url=os.getenv("MONGO_DB_URL") ## use it in each file to load it 
        mlops_pipeline_config =MLOpsPipelineConfig()
        data_ingestion_config=DataIngestionConfig(mlops_pipeline_config)
        data_ingestion=DataIngestion(data_ingestion_config,mongo_db_url)
        
        logging.info("Data Ingestion process started")
        print("Data Ingestion process started")
        data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
        logging.info("Data Ingestion process completed successfully")
        print("Data Ingestion process completed successfully")


    except Exception as e:
        raise NetworkSecurityException(e,sys)
    