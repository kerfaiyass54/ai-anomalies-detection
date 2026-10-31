# Grafana dashboards

Grafana provisions Elasticsearch data sources for the `logs` and `anomalies` indices, plus a dashboard named **Logs and Anomalies** in the **Anomaly Monitoring** folder. The dashboard refreshes every five seconds and shows the rolling anomaly rate, recent anomaly records, and recent Logstash log documents.

Detected anomaly records are persisted in PostgreSQL first. A separate migration worker copies pending records into the Elasticsearch `anomalies` index and marks them synced only after indexing succeeds. Failed migrations are retried, and existing PostgreSQL records are eligible for migration. Logstash currently indexes raw log events; anomaly detection runs when the anomaly API receives a file at `/api/v1/anomalies/detect` or an event at `/api/v1/anomalies/ingest`. The dashboard refreshes live as those services write data, but the current pipeline does not automatically send every Logstash event to the anomaly API.

Start or rebuild Grafana and its data sources with:

```sh
docker compose up -d --build grafana anomaly-detection anomaly-elasticsearch-migration elasticsearch
```

Open Grafana at `http://localhost:3000` and select **Dashboards > Anomaly Monitoring > Logs and Anomalies**. The configured Elasticsearch datasource uses Grafana's built-in Elasticsearch support and the `@timestamp` time field.
