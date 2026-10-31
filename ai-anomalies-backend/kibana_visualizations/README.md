# Kibana visualizations service

This read-only service retrieves saved `visualization` objects from the configured Kibana space using Kibana's Saved Objects API.

It reads classic saved visualization objects, including objects imported from `kibana/saved_objects/observability.ndjson`. Kibana marks the generic Saved Objects find API as deprecated; its newer Visualizations API lists Lens visualizations instead. If the project switches its saved charts to Lens, this service should be moved to that API.

## Start

From the repository root, run:

```sh
docker compose up -d --build kibana kibana-visualizations
```

The service listens on `http://localhost:8004` by default. Configure `KIBANA_URL`, `KIBANA_SPACE`, and, when Kibana authentication is enabled, either `KIBANA_API_KEY` or `KIBANA_USERNAME` plus `KIBANA_PASSWORD` in `.env`.

## Endpoints

- `GET /api/v1/kibana/visualizations?page=1&per_page=100` lists saved visualizations.
- `GET /api/v1/kibana/visualizations?search=anomaly` filters by title.
- `GET /api/v1/kibana/visualizations/{id}` returns one saved visualization.

Both list and detail responses include the visualization definition and its saved search source when Kibana provides them. Kibana must grant the configured credentials permission to read saved objects.
