import os
from functools import lru_cache

from elasticsearch import Elasticsearch


@lru_cache(maxsize=1)
def get_elasticsearch_client() -> Elasticsearch:
    return Elasticsearch(os.getenv("ELASTICSEARCH_URL", "http://localhost:9200"))
