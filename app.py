# Description: This file is the main file which is used to run the FastAPI application. It contains the routes for training and prediction.

# Importing Required Libraries
import sys
import os
import pymongo
from src.exception.exception import NetworkSecurityException
from src.logging.logger import logging
from src.pipeline.training_pipeline import TrainingPipeline
from src.constant.mlops_pipeline import DATA_INGESTION_COLLECTION_NAME
from src.constant.mlops_pipeline import DATA_INGESTION_DATABASE_NAME
from src.utils.main_utils.utils import load_object
from src.utils.ml_utils.model.estimator import NetworkModel

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, File, UploadFile,Request
from uvicorn import run as app_run
from fastapi.responses import Response
from starlette.responses import RedirectResponse
import pandas as pd
from dotenv import load_dotenv

# Load the environment variables
load_dotenv()
mongo_db_url = os.getenv("MONGO_DB_URL")
print(mongo_db_url)

# Connect to the MongoDB database
import certifi
ca = certifi.where()

# Connect to the MongoDB database
client = pymongo.MongoClient(mongo_db_url, tlsCAFile=ca)
database = client[DATA_INGESTION_DATABASE_NAME]
collection = database[DATA_INGESTION_COLLECTION_NAME]

# Create a FastAPI app
app = FastAPI()
origins = ["*"] # Allow all origins

# Add CORS middleware to the FastAPI app
"""This middleware will allow all origins to make requests to the FastAPI app. 
This is required as the FastAPI app will be running on a different port than the frontend application.
The frontend application will be running on port 3000 and the FastAPI app will be running on port 8000.
By default, browsers block requests from different origins due to security reasons.
The CORS middleware will add the necessary headers to the response to allow requests from different origins."""

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add routes to the FastAPI app
from fastapi.templating import Jinja2Templates # 
templates = Jinja2Templates(directory="./templates")

# Define the routes
@app.get("/", tags=["authentication"]) # This route will redirect to the documentation page
async def index():
    return RedirectResponse(url="/docs") # Redirect to the documentation page

@app.get("/train") # This route will be used to train the model
async def train_route(): # This function will be called when the /train route is hit
    try:
        train_pipeline=TrainingPipeline() # Create an instance of the TrainingPipeline class
        train_pipeline.run_pipeline() # Run the training pipeline
        return Response("Training is successful")
    except Exception as e:
        raise NetworkSecurityException(e,sys)
    
@app.post("/predict") # This route will be used to make predictions
async def predict_route(request: Request,file: UploadFile = File(...)): # This function will be called when the /predict route is hit
    try:
        df=pd.read_csv(file.file)
        #print(df)
        preprocesor=load_object("final_model/preprocessor.pkl")
        final_model=load_object("final_model/model.pkl")
        network_model = NetworkModel(preprocessor=preprocesor,model=final_model)
        print(df.iloc[0])
        y_pred = network_model.predict(df)
        print(y_pred)
        df['predicted_column'] = y_pred
        print(df['predicted_column'])
        #df['predicted_column'].replace(-1, 0)
        #return df.to_json()
        df.to_csv('prediction_output/output.csv')
        table_html = df.to_html(classes='table table-striped')
        #print(table_html)
        return templates.TemplateResponse("table.html", {"request": request, "table": table_html})
        
    except Exception as e:
            raise NetworkSecurityException(e,sys)
    
if __name__=="__main__":
    app_run(app,host="0.0.0.0",port=8080) # Run the FastAPI app on port 8000
