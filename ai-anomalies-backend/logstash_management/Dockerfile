FROM python:3.12-slim

WORKDIR /app
COPY logstash_management/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY logstash_management ./logstash_management

EXPOSE 8002
CMD ["uvicorn", "logstash_management.main:app", "--host", "0.0.0.0", "--port", "8002"]
