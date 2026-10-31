FROM python:3.12-slim

WORKDIR /app
COPY elasticsearch_logs/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY elasticsearch_logs ./elasticsearch_logs

EXPOSE 8003
CMD ["uvicorn", "elasticsearch_logs.main:app", "--host", "0.0.0.0", "--port", "8003"]
