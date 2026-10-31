# Logstash configuration service

This service manages the Logstash file input and Elasticsearch output settings. It writes a generated pipeline into the shared `logstash/pipeline` directory; Logstash reloads it automatically.

## Setup

1. Copy `.env.example` to `.env` if you have not already.
2. Set `LOGSTASH_CONFIG_TOKEN` to a long random value.
3. Set `CONTAINER_LOGS_HOST_PATH` to the host directory containing the logs. The service exposes it inside Logstash as `/var/log/containers`.
4. Start the services with `docker compose up -d --build logstash-management elasticsearch-logs`.

The API is available at `http://localhost:8002`. Send the configured token as a bearer token. For example:

```http
GET /api/v1/logstash/config
Authorization: Bearer <LOGSTASH_CONFIG_TOKEN>
```

Update settings with `PUT /api/v1/logstash/config`:

```json
{
  "settings": {
    "input_path": "/var/log/containers/*.log",
    "start_position": "beginning",
    "elasticsearch_index": "logs"
  }
}
```

Supported settings are intentionally limited to a file pattern under `/var/log/containers`, `beginning` or `end` as the start position, and a valid lowercase Elasticsearch index name. Send `{"settings": null}` to restore the default settings. The API reports a failed reload and restores the previous settings if Logstash does not accept the generated pipeline.

## Access

The API port is bound to localhost by Compose and requires the bearer token. Keep the token private and expose the service only through a trusted administrative path.
