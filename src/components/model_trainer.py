# Description: This file contains the ModelTrainer class which is responsible for training the model and saving the trained model.

# Importing Required Libraries
import os
import sys
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import AdaBoostClassifier,GradientBoostingClassifier,RandomForestClassifier
from src.exception.exception import NetworkSecurityException 
from src.logging.logger import logging
from src.entity.artifact_entity import DataTransformationArtifact,ModelTrainerArtifact
from src.entity.config_entity import ModelTrainerConfig
from src.utils.ml_utils.model.estimator import NetworkModel
from src.utils.main_utils.utils import save_object,load_object
from src.utils.main_utils.utils import load_numpy_array_data,evaluate_models
from src.utils.ml_utils.metric.classification_metric import get_classification_score
import mlflow
import yaml
from urllib.parse import urlparse
from dotenv import load_dotenv
import dagshub

load_dotenv()

# dagshub.init(repo_owner="Vipul111196", repo_name="End_to_End_Network_Security_Project", mlflow=True)


# os.environ["MLFLOW_TRACKING_URI"]= "http://127.0.0.1:5000" # Running Mlflow server on localhost

class ModelTrainer:
    def __init__(self,model_trainer_config:ModelTrainerConfig, data_transformation_artifact:DataTransformationArtifact):
        try:
            self.model_trainer_config=model_trainer_config
            self.data_transformation_artifact=data_transformation_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def track_mlflow(self,best_model,classificationmetric):
        mlflow.set_tracking_uri(os.environ["MLFLOW_TRACKING_URI"])
        mlflow.set_experiment("Network Security Models") # Name of the experiment
        tracking_url_type_store = urlparse(mlflow.get_tracking_uri()).scheme # get the store type
        self.best_model=best_model
        self.classificationmetric=classificationmetric
        
        with mlflow.start_run():
            f1_score=self.classificationmetric.f1_score
            precision_score=self.classificationmetric.precision_score
            recall_score=self.classificationmetric.recall_score

            mlflow.log_metric("f1_score",f1_score)
            mlflow.log_metric("precision",precision_score)
            mlflow.log_metric("recall_score",recall_score)

            # Model registry does not work with file store
            if tracking_url_type_store != "file":
                mlflow.sklearn.log_model(self.best_model, "model", registered_model_name="Best_Model")
            else:
                mlflow.sklearn.log_model(self.best_model, "model")
        
    def train_model(self,X_train,y_train,x_test,y_test):
        
        models = {
                "Random Forest": RandomForestClassifier(verbose=1),
                "Decision Tree": DecisionTreeClassifier(),
                "Gradient Boosting": GradientBoostingClassifier(verbose=1),
                "Logistic Regression": LogisticRegression(verbose=1),
                "AdaBoost": AdaBoostClassifier(),
            }
        
        logging.info("Models to be trained: {}".format(models.keys()))
        params= yaml.load(open("src/model_params/model_params.yaml"),Loader=yaml.FullLoader)

        model_report:dict=evaluate_models(X_train=X_train,y_train=y_train,X_test=x_test,y_test=y_test,
                                          models=models,param=params)
        
        logging.info("Model Training Done")
        ## To get best model score from dict
        best_model_score = max(sorted(model_report.values()))

        ## To get best model name from dict
        best_model_name = list(model_report.keys())[
            list(model_report.values()).index(best_model_score)
        ]
        best_model = models[best_model_name]

        logging.info(f"Best Model: {best_model_name}")
        logging.info(f"Best Model Score: {best_model_score}")
        # Get classification metric for train data
        y_train_pred=best_model.predict(X_train)
        classification_train_metric=get_classification_score(y_true=y_train,y_pred=y_train_pred)
        
        ## Track the experiements with mlflow
        logging.info("Tracking the training experiments with mlflow")
        self.track_mlflow(best_model,classification_train_metric)

        # Get classification metric for test data
        y_test_pred=best_model.predict(x_test)
        classification_test_metric=get_classification_score(y_true=y_test,y_pred=y_test_pred)

        ## Track the experiements with mlflow
        logging.info("Tracking the testing experiments with mlflow")
        self.track_mlflow(best_model,classification_test_metric)

        ## Load preprocessor object
        logging.info("Loading preprocessor object")
        preprocessor = load_object(file_path=self.data_transformation_artifact.transformed_object_file_path)

        ## Save the model  
        logging.info("Saving the trained model")
        model_dir_path = os.path.dirname(self.model_trainer_config.trained_model_file_path)
        os.makedirs(model_dir_path,exist_ok=True)

        Network_Model = NetworkModel(preprocessor=preprocessor,model=best_model)
        save_object(self.model_trainer_config.trained_model_file_path,obj=Network_Model)
        
        #model pusher
        logging.info("Pushing the model to the model local registry")
        save_object("final_model/model.pkl",best_model)
        
        ## Model Trainer Artifact
        model_trainer_artifact=ModelTrainerArtifact(trained_model_file_path=self.model_trainer_config.trained_model_file_path,
                             train_metric_artifact=classification_train_metric,
                             test_metric_artifact=classification_test_metric
                             )
        
        logging.info(f"Model trainer artifact: {model_trainer_artifact}")
        
        return model_trainer_artifact
        
    def initiate_model_trainer(self)->ModelTrainerArtifact:
        try:
            train_file_path = self.data_transformation_artifact.transformed_train_file_path
            test_file_path = self.data_transformation_artifact.transformed_test_file_path

            #loading training array and testing array
            train_arr = load_numpy_array_data(train_file_path)
            test_arr = load_numpy_array_data(test_file_path)

            x_train, y_train, x_test, y_test = (
                train_arr[:, :-1],
                train_arr[:, -1],
                test_arr[:, :-1],
                test_arr[:, -1],
            )

            model_trainer_artifact=self.train_model(x_train,y_train,x_test,y_test)
            return model_trainer_artifact

        except Exception as e:
            raise NetworkSecurityException(e,sys)