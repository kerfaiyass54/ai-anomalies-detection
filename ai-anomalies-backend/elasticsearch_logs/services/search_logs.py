import base64
import json
import os
from typing import Any

from elasticsearch import ElasticsearchException, NotFoundError

from ..errors import LogSearchError
from ..schemas import LogEntry, LogSearchPage
from .elasticsearch_client import get_elasticsearch_client

PIT_KEEP_ALIVE = "1m"


def _encode_cursor(pit_id: str, sort_values: list[Any]) -> str:
    value = json.dumps({"pit_id": pit_id, "search_after": sort_values}, separators=(",", ":")).encode("utf-8")
    return base64.urlsafe_b64encode(value).decode("ascii").rstrip("=")


def _decode_cursor(cursor: str) -> tuple[str, list[Any]]:
    try:
        padded = cursor + "=" * (-len(cursor) % 4)
        payload = json.loads(base64.urlsafe_b64decode(padded).decode("utf-8"))
        pit_id, search_after = payload["pit_id"], payload["search_after"]
        if not isinstance(pit_id, str) or not isinstance(search_after, list):
            raise ValueError
        return pit_id, search_after
    except (ValueError, TypeError, KeyError, json.JSONDecodeError) as exc:
        raise LogSearchError("Invalid or expired logs cursor.", status_code=400) from exc


def _close_pit(client: Elasticsearch, pit_id: str) -> None:
    try:
        client.close_point_in_time(id=pit_id)
    except ElasticsearchException:
        pass


def search_logs(*, size: int = 100, cursor: str | None = None) -> LogSearchPage:
    """Return one consistent, newest-first page of logs from Elasticsearch."""
    client = get_elasticsearch_client()
    index = os.getenv("ELASTICSEARCH_LOGS_INDEX", "logs")
    try:
        if cursor:
            pit_id, search_after = _decode_cursor(cursor)
        else:
            try:
                pit_id = client.open_point_in_time(index=index, keep_alive=PIT_KEEP_ALIVE)["id"]
            except NotFoundError:
                return LogSearchPage(total=0, logs=[], next_cursor=None)
            search_after = []

        search_options: dict[str, Any] = {
            "pit": {"id": pit_id, "keep_alive": PIT_KEEP_ALIVE},
            "query": {"match_all": {}},
            "size": size + 1,
            "sort": [
                {"@timestamp": {"order": "desc", "missing": "_last"}},
                {"_shard_doc": "desc"},
            ],
            "track_total_hits": True,
        }
        if search_after:
            search_options["search_after"] = search_after
        response = client.search(**search_options)
        pit_id = response.get("pit_id", pit_id)
        hits = response["hits"]["hits"]
        page_hits = hits[:size]
        total_value = response["hits"].get("total", 0)
        total = total_value.get("value", 0) if isinstance(total_value, dict) else int(total_value)
        has_more = len(hits) > size

        if has_more and page_hits:
            next_cursor = _encode_cursor(pit_id, page_hits[-1]["sort"])
        else:
            _close_pit(client, pit_id)
            next_cursor = None

        return LogSearchPage(
            total=total,
            logs=[
                LogEntry(id=hit["_id"], index=hit["_index"], source=hit.get("_source", {}))
                for hit in page_hits
            ],
            next_cursor=next_cursor,
        )
    except LogSearchError:
        raise
    except ElasticsearchException as exc:
        raise LogSearchError("Could not retrieve logs from Elasticsearch.") from exc
