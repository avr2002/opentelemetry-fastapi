"""Fixter for FastAPI test client."""

import pytest
from fastapi.testclient import TestClient
from otel_api.main import create_app


@pytest.fixture
def client() -> TestClient:
    app = create_app()
    with TestClient(app) as client:
        yield client
