# Phishing Website Detection — End-to-End MLOps Pipeline

ML pipeline for detecting phishing websites using URL, HTML, and domain-based features. Built with FastAPI, MLflow, MongoDB Atlas, AWS (S3/ECR/ECS), and a full monitoring stack (Prometheus + Grafana).

## Architecture

```
                    GitHub Actions CI/CD
                           |
         ┌─────────────────┼─────────────────┐
         v                 v                  v
    Lint + Test     Build Docker Image    Deploy to AWS ECS
                         |
                    Amazon ECR
                         |
    ┌────────────────────┼────────────────────┐
    v                    v                    v
  FastAPI App       MLflow Server      Prometheus + Grafana
  (port 8080)       (port 5000)        (ports 9090, 3000)
    |                    |
    v                    v
  MongoDB Atlas     Experiment Tracking
  (data source)     + Model Registry
    |
    v
  AWS S3
  (model artifacts)
```

## Pipeline Steps

```
MongoDB Atlas (raw data)
    |
    v
Data Ingestion ──> Data Validation ──> Data Transformation ──> Model Training
                                                                    |
                                                                    v
                                                              MLflow Tracking
                                                                    |
                                                                    v
                                                              AWS S3 (model artifacts)
                                                                    |
                                                                    v
                                                              FastAPI Prediction API
```

1. **Data Ingestion** — Pulls phishing dataset from MongoDB Atlas, splits into train/test
2. **Data Validation** — Schema validation against `data_schema/schema.yaml`, drift detection
3. **Data Transformation** — Feature engineering with KNN Imputer, preprocessing pipeline
4. **Model Training** — Trains classifiers, logs metrics to MLflow/DagsHub, uploads best model to S3

## Tech Stack

| Component | Technology |
|---|---|
| API | FastAPI |
| ML Training | scikit-learn |
| Experiment Tracking | MLflow + DagsHub |
| Data Versioning | DVC |
| Database | MongoDB Atlas |
| Model Storage | AWS S3 |
| Container Registry | Amazon ECR |
| Deployment | Amazon ECS |
| Monitoring | Prometheus + Grafana |
| CI/CD | GitHub Actions |
| Containerization | Docker + docker-compose |

## Quick Start

### Local

```bash
git clone https://github.com/Vipul111196/End_to_End_Network_Security_Project.git
cd End_to_End_Network_Security_Project

cp .env.example .env   # fill in your credentials
make install

# Train the model
make train

# Run the API
make run               # http://localhost:8080/docs
```

### Docker (full stack with monitoring)

```bash
cp .env.example .env   # fill in your credentials
make docker-up

# Access points:
# API:        http://localhost:8080/docs
# MLflow:     http://localhost:5000
# Prometheus: http://localhost:9090
# Grafana:    http://localhost:3000 (admin/admin)
```

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/docs` | Swagger UI |
| GET | `/train` | Trigger training pipeline |
| POST | `/predict` | Upload CSV for batch prediction |
| POST | `/predict-instance` | Single instance prediction |
| GET | `/metrics` | Prometheus metrics |

## Monitoring

The Grafana dashboard tracks:
- **Request rate** per endpoint
- **Response latency** (p95)
- **Requests in progress**
- **Error rate** (5xx)

Prometheus scrapes the `/metrics` endpoint exposed by FastAPI every 15s.

## Dataset

Phishing Websites Dataset by Rami M. Mohammad, Fadi Thabtah, and Lee McCluskey. Features include URL structure analysis, HTML/JavaScript indicators, and domain registration data.

## Project Structure

```
├── app.py                          # FastAPI application
├── main.py                         # Training pipeline entry point
├── src/
│   ├── components/
│   │   ├── data_ingestion.py       # MongoDB data extraction
│   │   ├── data_validation.py      # Schema + drift checks
│   │   ├── data_transformation.py  # Feature engineering
│   │   └── model_trainer.py        # Model training + MLflow logging
│   ├── pipeline/
│   │   └── training_pipeline.py    # Orchestrates all components
│   ├── entity/                     # Config + artifact dataclasses
│   ├── cloud/                      # S3 sync utilities
│   ├── utils/                      # ML metrics, model loading
│   ├── exception/                  # Custom exception handling
│   └── logging/                    # Logger config
├── monitoring/
│   ├── prometheus.yml              # Prometheus scrape config
│   └── grafana/                    # Grafana dashboards + provisioning
├── data_engineering_pipeline/      # ETL scripts for MongoDB
├── .github/workflows/main.yaml    # CI/CD pipeline
├── Dockerfile
├── docker-compose.yml
├── Makefile
└── .env.example
```

## CI/CD

GitHub Actions pipeline on push to `main`:
1. **CI** — Lint + unit tests
2. **CD** — Build Docker image, push to ECR, deploy to ECS

## License

MIT
