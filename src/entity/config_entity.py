# Description: Configuration entity for entire MLOps pipeline.

# Importing Required Libraries
from datetime import datetime
import os
from src.constant import mlops_pipeline

# print(mlops_pipeline.PIPELINE_NAME)
# print(mlops_pipeline.ARTIFACT_DIR)

# Defining the configuration entity for the training pipeline
class MLOpsPipelineConfig: #
    def __init__(self,timestamp=datetime.now()):
        timestamp=timestamp.strftime("%m_%d_%Y_%H_%M_%S")
        self.timestamp: str=timestamp
        self.pipeline_name=mlops_pipeline.PIPELINE_NAME
        self.artifact_name=mlops_pipeline.ARTIFACT_DIR
        self.artifact_dir=os.path.join(self.artifact_name,self.timestamp) # Create a directory with timestamp
        self.model_dir=os.path.join("final_model")

# Data Ingestion Configuration
class DataIngestionConfig:
    def __init__(self,training_pipeline_config : MLOpsPipelineConfig):
        self.data_ingestion_dir: str = os.path.join(training_pipeline_config.artifact_dir,mlops_pipeline.DATA_INGESTION_DIR_NAME)
        self.feature_store_file_path: str = os.path.join(self.data_ingestion_dir, mlops_pipeline.DATA_INGESTION_FEATURE_STORE_DIR, mlops_pipeline.FILE_NAME)
        self.training_file_path: str = os.path.join(self.data_ingestion_dir, mlops_pipeline.DATA_INGESTION_INGESTED_DIR, mlops_pipeline.TRAIN_FILE_NAME)
        self.testing_file_path: str = os.path.join(self.data_ingestion_dir, mlops_pipeline.DATA_INGESTION_INGESTED_DIR, mlops_pipeline.TEST_FILE_NAME)
        self.train_test_split_ratio: float = mlops_pipeline.DATA_INGESTION_TRAIN_TEST_SPLIT_RATION
        self.collection_name: str = mlops_pipeline.DATA_INGESTION_COLLECTION_NAME
        self.database_name: str = mlops_pipeline.DATA_INGESTION_DATABASE_NAME

if __name__=="__main__":
    pass