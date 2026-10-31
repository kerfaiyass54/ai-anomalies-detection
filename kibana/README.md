# Kibana visualizations

Compose already connects Kibana to Elasticsearch at `http://elasticsearch:9200` on the observability network. From the host, open Kibana at `http://localhost:5601`.

## Import the saved visualizations

1. Start Kibana and Elasticsearch: `docker compose up -d elasticsearch kibana`.
2. In Kibana, open **Stack Management > Saved Objects** and select **Import**.
3. Import [`saved_objects/observability.ndjson`](saved_objects/observability.ndjson).
4. Open **Analytics > Dashboard** and select **Logs and Anomaly Operations**.

The import creates data views for `logs` and `anomalies`, along with these visualizations:

- Log error trend (`message` containing error, exception, or failed)
- Total log volume over time
- Anomaly count over time
- Anomaly count by source type

Use the dashboard time picker to change the default 24-hour range. To refresh while the dashboard is open, enable dashboard auto-refresh in Kibana's time picker.

The `logs` index is written by Logstash. The `anomalies` index is populated by the PostgreSQL-to-Elasticsearch migration worker, so its visualizations remain empty until anomaly records have migrated. Kibana's built-in Elasticsearch integration uses the `@timestamp` field for both data views.
