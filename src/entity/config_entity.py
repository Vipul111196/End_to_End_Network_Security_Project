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

if __name__=="__main__":
    pass