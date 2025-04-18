FROM python:3.10-slim-buster

WORKDIR /app
COPY . /app

# Install git and awscli
RUN apt-get update && apt-get install -y git awscli

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python3", "app.py"]
