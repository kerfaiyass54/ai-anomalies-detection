# Elasticsearch logs service

This read-only service retrieves documents from the Elasticsearch index selected by `ELASTICSEARCH_LOGS_INDEX` (default: `logs`).

Start it with:

```sh
docker compose up -d --build elasticsearch-logs
```

The API is available at `http://localhost:8003`. Request `GET /api/v1/logs?size=100`; `size` may be from 1 to 1000. Each response includes the matching logs and a `next_cursor` when another page is available. Pass that cursor unchanged as `cursor` on the next request. Continue until `next_cursor` is `null`.

The service reads Elasticsearch only and does not modify or delete log documents.
