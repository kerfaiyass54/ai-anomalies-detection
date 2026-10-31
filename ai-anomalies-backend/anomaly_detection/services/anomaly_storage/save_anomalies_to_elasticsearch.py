import logging
import os

from elasticsearch import Elasticsearch, ElasticsearchException

from ...schemas.anomaly import AnomalyRecord

logger = logging.getLogger(__name__)


def save_anomalies_to_elasticsearch(records: list[AnomalyRecord]) -> None:
    """Best-effort index of saved anomaly records for Grafana and search."""
    if not records:
        return

    client = Elasticsearch(os.getenv("ELASTICSEARCH_URL", "http://elasticsearch:9200"))
    try:
        for record in records:
            client.index(
                index=os.getenv("ELASTICSEARCH_ANOMALIES_INDEX", "anomalies"),
                id=str(record.id),
                document={
                    "@timestamp": record.occurred_at,
                    "event": {"kind": "alert", "category": ["anomaly"]},
                    "source_type": record.source_type,
                    "details": record.details,
                    "score": record.score,
                },
            )
    except ElasticsearchException:
        logger.exception("Could not index anomaly documents in Elasticsearch.")
    finally:
        client.close()
