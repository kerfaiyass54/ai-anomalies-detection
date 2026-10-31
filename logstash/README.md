# Logstash log ingestion

Logstash listens for Beats events on port `5044`. It keeps sending events to Elasticsearch and also posts supported log events to the anomaly detection API. The pipeline is in `pipeline/logstash.conf` and is mounted read-only by Compose.

## Start the services

Copy the repository's `.env.example` to `.env` and replace the placeholder passwords. Start PostgreSQL and the anomaly API first:

```powershell
docker compose up -d --build postgresql anomaly-detection
```

Register a model before sending live events. Model training uses the uploaded text file endpoint and requires at least four non-empty lines:

```powershell
curl.exe -X POST "http://127.0.0.1:8001/api/v1/anomalies/detect?source_type=docker" -F "file=@.\logs.txt"
```

Then start Logstash:

```powershell
docker compose up -d --build logstash
```

The Logstash output posts each event to `http://anomaly-detection:8001/api/v1/anomalies/ingest` on the Compose network. The API scores it with the latest registered model and saves detected lines to PostgreSQL. Elasticsearch continues to receive every event, including events without a recognized source type.

## Source type

Beats should set `source_type` to `k8s`, `docker`, or `jenkins`. Logstash also infers it from Kubernetes metadata, Docker/container metadata, the `service.type` field, or a `jenkins` tag. Unrecognized events are indexed in Elasticsearch but are not sent to the anomaly API.

For Filebeat, set an explicit source type with:

```yaml
fields:
  source_type: docker
fields_under_root: true
output.logstash:
  hosts: ["localhost:5044"]
```

Use `source_type: jenkins` or `source_type: k8s` for those sources. Log events should include a `message` field; `@timestamp` is passed through as the event time.
