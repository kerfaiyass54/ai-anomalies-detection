import os

from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from sqlalchemy import text

from .database import get_database_engine
from .schema import ensure_anomalies_table


def migrate_anomalies_to_elasticsearch(*, batch_size: int = 500) -> int:
    """Copy pending PostgreSQL rows to Elasticsearch, then mark them synced."""
    engine = get_database_engine()
    client = Elasticsearch(os.getenv("ELASTICSEARCH_URL", "http://elasticsearch:9200"))
    try:
        with engine.begin() as connection:
            ensure_anomalies_table(connection)
            rows = connection.execute(text("""
                SELECT id, occurred_at, source_type, details, score
                FROM detected_anomalies
                WHERE elasticsearch_synced_at IS NULL
                ORDER BY id
                LIMIT :batch_size
                FOR UPDATE SKIP LOCKED
            """), {"batch_size": batch_size}).mappings().all()
            if not rows:
                return 0

            actions = [
                {
                    "_index": os.getenv("ELASTICSEARCH_ANOMALIES_INDEX", "anomalies"),
                    "_id": str(row["id"]),
                    "_source": {
                        "@timestamp": row["occurred_at"],
                        "event": {"kind": "alert", "category": ["anomaly"]},
                        "source_type": row["source_type"],
                        "details": row["details"],
                        "score": row["score"],
                    },
                }
                for row in rows
            ]
            bulk(client, actions, raise_on_error=True, raise_on_exception=True)
            connection.execute(
                text("""
                    UPDATE detected_anomalies
                    SET elasticsearch_synced_at = NOW()
                    WHERE id = :id
                """),
                [{"id": row["id"]} for row in rows],
            )
            return len(rows)
    finally:
        client.close()
