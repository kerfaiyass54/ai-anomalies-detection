FROM python:3.12-slim

WORKDIR /app
COPY anomaly_detection/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY anomaly_detection ./anomaly_detection

EXPOSE 8001
CMD ["uvicorn", "anomaly_detection.main:app", "--host", "0.0.0.0", "--port", "8001"]
