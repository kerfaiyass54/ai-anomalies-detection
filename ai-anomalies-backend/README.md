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

## Runtime inspection API

The backend host must have the Docker CLI configured to reach its Docker daemon. For Kubernetes endpoints, `kubectl` must be installed and have a valid kubeconfig/current context. The API executes these local CLIs with argument arrays (without a shell), applies a command timeout, and returns command failures as HTTP errors.

| Method | Path | Purpose |
| --- | --- | --- |
| `GET` | `/api/v1/runtime/containers` | List running and stopped Docker containers. Each result includes `running`. |
| `GET` | `/api/v1/runtime/containers/{container_id}/logs?tail=200` | Get recent logs by container ID or name. |
| `GET` | `/api/v1/runtime/pods?namespace=default` | List pods in a namespace; omit `namespace` to list across namespaces. |
| `GET` | `/api/v1/runtime/pods/{pod_name}/logs?namespace=default&container=worker&tail=200` | Get logs for a pod, optionally selecting one of its containers. |

The log endpoints return plain text. `tail` is limited to 1–10,000 lines. Access to this API should be restricted to trusted users because runtime logs can contain sensitive data and the configured CLIs inherit the backend process's permissions.
