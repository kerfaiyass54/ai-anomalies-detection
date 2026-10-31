# AI Anomalies Backend

## Run the API

Install the Python dependencies, then start the development server from this directory:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m uvicorn ai_anomalies_backend.main:app --reload
```

The interactive API documentation is available at `http://127.0.0.1:8000/docs`.

## Standalone anomaly detection service

The anomaly detector is a separate service under `anomaly_detection/`. From the repository root, start PostgreSQL with `docker compose up -d postgresql`, then run the API from the backend directory:

```powershell
Set-Location ai-anomalies-backend
python -m pip install -r anomaly_detection/requirements.txt
python -m uvicorn anomaly_detection.main:app --reload --port 8001
```

Its API documentation is at `http://127.0.0.1:8001/docs`. `POST /api/v1/anomalies/detect?source_type=k8s` accepts a `.txt` multipart field named `file`; supported types are `k8s`, `docker`, and `jenkins`. It preprocesses and splits the lines, trains a TF-IDF and Isolation Forest pipeline, registers a version in MLflow, scores the logs, and stores detected lines in PostgreSQL with event time, source type, details, and score. A minimum of four non-empty lines and a maximum file size of 10 MB apply.

The service reads database settings from the repository-level `.env` (`POSTGRES_HOST`, `POSTGRES_PORT`, `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`, or `DATABASE_URL`). MLflow defaults to a local SQLite registry in the current working directory. Run the complete containerized service and database with `docker compose up --build anomaly-detection`.

Example upload from the repository root:

```powershell
curl.exe -X POST "http://127.0.0.1:8001/api/v1/anomalies/detect?source_type=docker" -F "file=@.\logs.txt"
```

## Runtime inspection API

The backend host must have the Docker CLI configured to reach its Docker daemon. For Kubernetes endpoints, `kubectl` must be installed and have a valid kubeconfig/current context. The API executes these local CLIs with argument arrays (without a shell), applies a command timeout, and returns command failures as HTTP errors.

| Method | Path | Purpose |
| --- | --- | --- |
| `GET` | `/api/v1/runtime/containers` | List running and stopped Docker containers. Each result includes `running`. |
| `GET` | `/api/v1/runtime/containers/{container_id}/logs?tail=200` | Get recent logs by container ID or name. |
| `GET` | `/api/v1/runtime/pods?namespace=default` | List pods in a namespace; omit `namespace` to list across namespaces. |
| `GET` | `/api/v1/runtime/pods/{pod_name}/logs?namespace=default&container=worker&tail=200` | Get logs for a pod, optionally selecting one of its containers. |

The log endpoints return plain text. `tail` is limited to 1–10,000 lines. Access to this API should be restricted to trusted users because runtime logs can contain sensitive data and the configured CLIs inherit the backend process's permissions.
