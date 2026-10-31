from sqlalchemy import Connection, text


def ensure_evaluations_table(connection: Connection) -> None:
    connection.execute(text("""
        CREATE TABLE IF NOT EXISTS model_evaluations (
            id BIGSERIAL PRIMARY KEY,
            evaluated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
            source_type VARCHAR(16) NOT NULL CHECK (source_type IN ('k8s', 'docker', 'jenkins')),
            model_name VARCHAR(255) NOT NULL,
            model_version VARCHAR(64) NOT NULL,
            logs_evaluated INTEGER NOT NULL CHECK (logs_evaluated > 0),
            anomalies_detected INTEGER NOT NULL CHECK (anomalies_detected >= 0),
            anomaly_rate DOUBLE PRECISION NOT NULL CHECK (anomaly_rate >= 0 AND anomaly_rate <= 1),
            mean_score DOUBLE PRECISION NOT NULL,
            median_score DOUBLE PRECISION NOT NULL,
            min_score DOUBLE PRECISION NOT NULL,
            max_score DOUBLE PRECISION NOT NULL,
            dataset_sha256 CHAR(64) NOT NULL
        )
    """))
