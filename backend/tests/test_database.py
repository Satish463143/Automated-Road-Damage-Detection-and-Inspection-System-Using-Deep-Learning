import os

import pytest
from sqlalchemy import text

from app.db.session import SessionLocal


@pytest.mark.skipif(
    os.getenv("RUN_DB_TESTS") != "1",
    reason="Set RUN_DB_TESTS=1 to run PostgreSQL integration tests.",
)
def test_database_connection():
    with SessionLocal() as db:
        value = db.scalar(text("SELECT 1"))
        assert value == 1
