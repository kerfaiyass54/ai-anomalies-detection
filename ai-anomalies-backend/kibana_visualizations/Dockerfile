FROM python:3.12-slim

WORKDIR /app
COPY kibana_visualizations/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY kibana_visualizations ./kibana_visualizations

EXPOSE 8004
CMD ["uvicorn", "kibana_visualizations.main:app", "--host", "0.0.0.0", "--port", "8004"]
