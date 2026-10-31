# Anomaly monitoring

Prometheus scrapes `anomaly-detection:8001/api/v1/anomalies/metrics`. The API exports `anomaly_rate`, the number of anomalies detected in the preceding 60 seconds. The rule in `rules/anomaly_detection.yml` fires when that value stays above 5 for one minute.

Prometheus forwards firing alerts to Alertmanager. Alertmanager groups `AnomalyDetected` alerts under the `anomaly-alerts` receiver. Add a notification integration (such as email, a webhook, or a chat receiver) to `alertmanager/alertmanager.yml` when its destination and credentials are available; the current receiver routes and groups alerts but does not send external notifications.

Start or rebuild the monitoring services with:

```sh
docker compose up -d --build anomaly-detection prometheus alertmanager
```

Prometheus is available at `http://localhost:9090`; Alertmanager is available at `http://localhost:9093`.
