import os
from functools import lru_cache

from sqlalchemy import URL, create_engine
from sqlalchemy.engine import Engine


@lru_cache(maxsize=1)
def get_database_engine() -> Engine:
    database_url = os.getenv("DATABASE_URL")
    if database_url:
        return create_engine(database_url, pool_pre_ping=True)
    return create_engine(
        URL.create(
            "postgresql+psycopg",
            username=os.getenv("POSTGRES_USER", "anomalies"),
            password=os.getenv("POSTGRES_PASSWORD", "anomalies"),
            host=os.getenv("POSTGRES_HOST", "localhost"),
            port=int(os.getenv("POSTGRES_PORT", "5432")),
            database=os.getenv("POSTGRES_DB", "anomalies"),
        ),
        pool_pre_ping=True,
    )
