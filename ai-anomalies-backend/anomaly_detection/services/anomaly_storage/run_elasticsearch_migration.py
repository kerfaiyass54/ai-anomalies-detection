import logging
import time

from .migrate_anomalies_to_elasticsearch import migrate_anomalies_to_elasticsearch

POLL_INTERVAL_SECONDS = 5
logger = logging.getLogger(__name__)


def run() -> None:
    logging.basicConfig(level=logging.INFO)
    logger.info("Starting PostgreSQL to Elasticsearch anomaly migration worker")
    while True:
        try:
            migrated = migrate_anomalies_to_elasticsearch()
            if migrated:
                logger.info("Migrated %s anomaly records to Elasticsearch", migrated)
        except Exception:
            logger.exception("Anomaly migration failed; pending rows will be retried")
        time.sleep(POLL_INTERVAL_SECONDS)


if __name__ == "__main__":
    run()
