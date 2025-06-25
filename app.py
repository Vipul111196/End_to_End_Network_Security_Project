import sys
import os
import pymongo
import certifi
import pandas as pd
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import List
from fastapi import FastAPI, File, UploadFile, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.responses import Response
from starlette.responses import RedirectResponse
from uvicorn import run as app_run

from src.exception.exception import NetworkSecurityException
from src.logging.logger import logging
from src.pipeline.training_pipeline import TrainingPipeline
from src.constant.mlops_pipeline import DATA_INGESTION_COLLECTION_NAME
from src.constant.mlops_pipeline import DATA_INGESTION_DATABASE_NAME
from src.utils.main_utils.utils import load_object, download_from_s3
from src.utils.ml_utils.model.estimator import NetworkModel
from prometheus_fastapi_instrumentator import Instrumentator

load_dotenv()
mongo_db_url = os.getenv("MONGO_DB_URL")
bucket_name = os.getenv("MODEL_BUCKET")

ca = certifi.where()
client = pymongo.MongoClient(mongo_db_url, tlsCAFile=ca)
database = client[DATA_INGESTION_DATABASE_NAME]
collection = database[DATA_INGESTION_COLLECTION_NAME]

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

templates = Jinja2Templates(directory="./templates")

# Prometheus metrics at /metrics
Instrumentator().instrument(app).expose(app)


@app.get("/", tags=["authentication"])
async def index():
    return RedirectResponse(url="/docs")


@app.get("/train")
async def train_route():
    try:
        train_pipeline = TrainingPipeline()
        train_pipeline.run_pipeline()
        return Response("Training is successful")
    except Exception as e:
        raise NetworkSecurityException(e, sys)


@app.post("/predict")
async def predict_route(request: Request, file: UploadFile = File(...)):
    try:
        bucket_name = os.getenv("TRAINING_BUCKET_NAME")
        df = pd.read_csv(file.file)

        download_from_s3(bucket_name, "final_model/latest/preprocessor.pkl", "final_model/preprocessor.pkl")
        download_from_s3(bucket_name, "final_model/latest/model.pkl", "final_model/model.pkl")

        preprocessor = load_object("final_model/preprocessor.pkl")
        final_model = load_object("final_model/model.pkl")
        network_model = NetworkModel(preprocessor=preprocessor, model=final_model)

        y_pred = network_model.predict(df)
        df['predicted_column'] = y_pred

        df.to_csv('prediction_output/output.csv')
        table_html = df.to_html(classes='table table-striped')
        return templates.TemplateResponse("table.html", {"request": request, "table": table_html})

    except Exception as e:
        raise NetworkSecurityException(e, sys)


class InstanceInput(BaseModel):
    features: List[float]


@app.post("/predict-instance")
async def predict_instance(input: InstanceInput):
    try:
        bucket_name = os.getenv("TRAINING_BUCKET_NAME")
        download_from_s3(bucket_name, "final_model/latest/preprocessor.pkl", "final_model/preprocessor.pkl")
        download_from_s3(bucket_name, "final_model/latest/model.pkl", "final_model/model.pkl")

        preprocessor = load_object("final_model/preprocessor.pkl")
        model = load_object("final_model/model.pkl")
        network_model = NetworkModel(preprocessor=preprocessor, model=model)

        prediction = network_model.predict_instance([input.features])
        return {"prediction": int(prediction[0])}

    except Exception as e:
        raise NetworkSecurityException(e, sys)


if __name__ == "__main__":
    app_run(app, host="0.0.0.0", port=8080)
