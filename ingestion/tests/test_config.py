"""Database driver selection remains stable across SQLAlchemy upgrades."""

import pytest
from sqlalchemy import create_engine

from src.config import Settings


@pytest.mark.parametrize(
    ("dsn", "expected"),
    [
        (
            "postgresql://user:pass@localhost/db",
            "postgresql+psycopg2://user:pass@localhost/db",
        ),
        (
            "postgresql+psycopg2://user:pass@localhost/db",
            "postgresql+psycopg2://user:pass@localhost/db",
        ),
        (
            "postgresql+psycopg://user:pass@localhost/db",
            "postgresql+psycopg://user:pass@localhost/db",
        ),
        ("sqlite:///:memory:", "sqlite:///:memory:"),
    ],
)
def test_postgres_driver_selection(dsn, expected):
    assert Settings(postgres_dsn=dsn).postgres_dsn == expected


def test_default_postgres_driver(monkeypatch):
    monkeypatch.delenv("POSTGRES_DSN", raising=False)
    engine = create_engine(Settings().postgres_dsn)
    assert engine.dialect.driver == "psycopg2"
    engine.dispose()


def test_environment_postgres_driver(monkeypatch):
    monkeypatch.setenv("POSTGRES_DSN", "postgresql://user:pass@database/db")
    assert Settings().postgres_dsn == "postgresql+psycopg2://user:pass@database/db"
