from sqlalchemy import Connection, text


def ensure_evaluations_table(connection: Connection) -> None:
    connection.execute(text("""
        CREATE TABLE IF NOT EXISTS model_evaluation_metrics (
            id BIGSERIAL PRIMARY KEY,
            evaluated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
            model_name VARCHAR(255) NOT NULL,
            model_version VARCHAR(64) NOT NULL,
            samples_evaluated INTEGER NOT NULL CHECK (samples_evaluated > 0),
            precision_score DOUBLE PRECISION NOT NULL CHECK (precision_score >= 0 AND precision_score <= 1),
            recall_score DOUBLE PRECISION NOT NULL CHECK (recall_score >= 0 AND recall_score <= 1),
            f1_score DOUBLE PRECISION NOT NULL CHECK (f1_score >= 0 AND f1_score <= 1),
            classification_report JSONB NOT NULL,
            input_sha256 CHAR(64) NOT NULL
        )
    """))
