# End to End - Network Security - Phishing Websites Detection Project

This project leverages machine learning to detect phishing websites by analyzing URL, HTML, and domain-based features. It is powered by **FastAPI**, **MLflow**, **DVC**, **DagsHub**, **MongoDB Atlas**, **AWS S3**, **Amazon ECR and ECS**, and **GitHub Actions** for a fully integrated and automated solution. The **Phishing Websites Dataset** used here was created by Rami M. Mohammad, Fadi Thabtah, and Lee McCluskey. The project enables training, testing, and deployment of a phishing detection model through a streamlined pipeline.

## Table of Contents
- [Project Overview](#project-overview)
- [Technologies Used](#technologies-used)
- [Dataset](#dataset)
- [Features](#features)
- [Usage](#usage)
- [CI/CD Pipeline](#ci-cd-pipeline)
- [References](#references)
- [Contributing](#contributing)
- [License](#license)

---

## Project Overview

This project aims to classify websites as either phishing or legitimate by using machine learning models built on URL, HTML, and domain-based features. The solution includes a FastAPI-based application for training and testing, as well as comprehensive data versioning, experiment tracking, and deployment support. It integrates data processing with MongoDB Atlas and S3-hosted datasets managed by DVC and DagsHub, and it automates deployment to **Amazon ECR** and **ECS** for scalable containerized applications.

## Technologies Used

This project utilizes the following tools and frameworks for a fully automated, scalable solution:

- **FastAPI**: Serves as the web framework for API endpoints, allowing users to train and test the phishing detection model.
- **MLflow**: Tracks model experiments, registers the best model, and stores experiment metrics for evaluation and improvement.
- **DVC**: Handles data versioning to ensure reliable dataset management and tracks processed data changes over time.
- **DagsHub**: Hosts processed data for easy access and version control, integrating with DVC for tracking changes stored in an AWS S3 bucket.
- **MongoDB Atlas**: Stores processed data in a secure, cloud-based NoSQL database, providing a source of truth for preprocessed data used in training.
- **Amazon ECR and ECS**: Manages and deploys Docker images, with ECR serving as the image registry and ECS hosting the model for live inference and scalability.
- **Docker**: A Dockerfile is used to containerize the FastAPI application, ensuring consistent deployment across environments.
- **GitHub Actions**: Facilitates CI/CD workflows to build, test, and deploy the application on AWS with automated integration.

## Dataset

The dataset, Phishing Websites Dataset, contains several feature columns that indicate various attributes and characteristics of URLs. These features include:

- **Address Bar-based Features:** Checks for IP addresses, URL length, and the presence of certain symbols.
- **HTML and JavaScript-based Features:** Includes indicators like the use of iframes, JavaScript events like onmouseover, and the disabling of right-clicks.
- **Domain-based Features:** Considers domain registration length, age, DNS records, and web traffic.
  
This dataset has been invaluable in building and testing a model to distinguish between phishing and legitimate websites.

## Features

Each row in the dataset represents a website and its specific characteristics. The following are some of the key features used in this project:

- **having_IP_Address:** Indicates if an IP address is used instead of a domain name.
- **URL_Length:** Measures the URL length, which can indicate if the URL is suspicious.
- **Shortining_Service:** Identifies the use of URL shortening services.
- **having_At_Symbol:** Checks for the presence of the "@" symbol.
- **double_slash_redirecting:** Indicates double slash redirection in the URL.
- **Prefix_Suffix:** Flags the use of suspicious prefixes or suffixes.
- **having_Sub_Domain:** Detects the use of multiple subdomains.
- **SSLfinal_State:** Examines the SSL certificate to evaluate security.
- **Domain_registeration_length:** Considers domain registration duration.
- **Favicon:** Identifies if the favicon is loaded from a different domain.
- **HTTPS_token:** Checks if "HTTPS" is used in the domain name.
- **web_traffic:** Measures web traffic data.
- **Google_Index:** Determines if the URL is indexed by Google.
- **Result:** The final classification, identifying the website as phishing or legitimate.
These and other features collectively contribute to the detection of phishing websites by identifying common patterns and anomalies in the URLs and site content.

## Usage

### Setup

To use this project:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Vipul111196/End_to_End_Network_Security_Project.git
   cd End_to_End_Network_Security_Project
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the FastAPI Application**:
   The FastAPI app provides an interface for training and testing the phishing detection model. You can start it with:
   ```bash
   uvicorn app.main:app --reload
   ```

4. **Data Versioning with DVC**:
   The dataset is versioned using DVC and hosted on **DagsHub** with an S3 bucket as the storage backend. To pull the latest version:
   ```bash
   dvc pull
   ```

5. **Experiment Tracking with MLflow**:
   Experiments are tracked in **MLflow**, and the best model is registered for deployment. You can view experiment metrics by running in DagsHub

6. **Database Integration**:
   - Processed data is stored in **MongoDB Atlas**, making it accessible for model training and testing.
   - Data from MongoDB Atlas can be fetched and processed as part of the ETL pipeline.

### Docker Setup

The application is containerized using Docker. You can build and run the Docker image with:
```bash
docker build -t End_to_End_Network_Security_Project .
docker run -p 8080:8080 End_to_End_Network_Security_Project
```

## CI/CD Pipeline

This project includes a **GitHub Actions** workflow for CI/CD to ensure smooth integration, testing, and deployment. The workflow includes the following steps:

1. **Continuous Integration (CI)**:
   - Lints code to enforce code standards.
   - Runs unit tests to ensure code correctness.

2. **Continuous Delivery (CD)**:
   - Builds and tags a Docker image.
   - Pushes the Docker image to **Amazon ECR** (Elastic Container Registry).
   - Deploys the latest image to **AWS ECS** (Elastic Container Service) to serve the application.

The GitHub Actions CI/CD pipeline manages automated deployment, scaling, and updating of the phishing detection application on AWS, ensuring high availability for users.

## References

This project is based on research by:

- **Rami M. Mohammad**, University of Huddersfield
- **Fadi Thabtah**, Canadian University of Dubai
- **Lee McCluskey**, University of Huddersfield

For more details, refer to the "Phishing Websites Features" documentation included with the dataset.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your changes.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.

---

This README now includes references to Amazon ECR and ECS at the beginning and does not include the workflow specifics. Let me know if further adjustments are needed!
