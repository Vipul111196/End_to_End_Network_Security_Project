import os
import sys
from src.logging.logger import logging 
from src.exception.exception import NetworkSecurityException
from src.entity.config_entity import MLOpsPipelineConfig, DataIngestionConfig, DataValidationConfig, DataTransformationConfig
from src.entity.artifact_entity import DataIngestionArtifact
from src.components.data_ingestion import DataIngestion
from src.components.data_validation import DataValidation
from src.components.data_transformation import DataTransformation
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

        # Data Validation Process
        data_validation_config = DataValidationConfig(mlops_pipeline_config)
        validation_data = DataValidation(data_ingestion_artifact, data_validation_config)
        logging.info("Data Validation process started")
        print("Data Validation process started")
        validation_data_artifact = validation_data.initiate_data_validation()
        logging.info("Data Validation process completed successfully")
        print("Data Validation process completed successfully")

        # Data Transformation Process
        data_transformation_config = DataTransformationConfig(mlops_pipeline_config)
        data_tranformation = DataTransformation(validation_data_artifact, data_transformation_config)
        logging.info("Data Transformation process started")
        print("Data Transformation process started")
        data_transformation_artifact = data_tranformation.initiate_data_transformation()
        logging.info("Data Transformation process completed successfully")
        print("Data Transformation process completed successfully")

    except Exception as e:
        raise NetworkSecurityException(e,sys)
    