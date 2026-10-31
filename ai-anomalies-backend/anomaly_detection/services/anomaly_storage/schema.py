from sqlalchemy import Connection, text


def ensure_anomalies_table(connection: Connection) -> None:
    connection.execute(text("""
        CREATE TABLE IF NOT EXISTS detected_anomalies (
            id BIGSERIAL PRIMARY KEY,
            occurred_at TIMESTAMPTZ NOT NULL,
            source_type VARCHAR(16) NOT NULL CHECK (source_type IN ('k8s', 'docker', 'jenkins')),
            details TEXT NOT NULL,
            score DOUBLE PRECISION NOT NULL,
            created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
            elasticsearch_synced_at TIMESTAMPTZ
        )
    """))
    connection.execute(text("""
        ALTER TABLE detected_anomalies
        ADD COLUMN IF NOT EXISTS elasticsearch_synced_at TIMESTAMPTZ
    """))
