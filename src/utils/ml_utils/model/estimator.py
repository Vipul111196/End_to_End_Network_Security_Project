from src.constant.mlops_pipeline import SAVED_MODEL_DIR,MODEL_FILE_NAME
from typing import List
import os
import sys

from src.exception.exception import NetworkSecurityException
from src.logging.logger import logging

class NetworkModel:
    def __init__(self,preprocessor,model):
        try:
            self.preprocessor = preprocessor
            self.model = model
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    def predict(self,x):
        try:
            x_transform = self.preprocessor.transform(x)
            y_hat = self.model.predict(x_transform)
            return y_hat
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def predict_instance(self, data: List[List[float]]) -> List[int]:
        transformed = self.preprocessor.transform(data)
        return self.model.predict(transformed)
