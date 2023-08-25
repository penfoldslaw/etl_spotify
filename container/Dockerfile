# Dockerfile
FROM python:3.8

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY etl/etl.py .


CMD ["python", "real_etl.py"]
