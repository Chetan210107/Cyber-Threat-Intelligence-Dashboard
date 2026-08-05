from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import pytest

from backend.app import create_app
from backend.config import TestingConfig
from backend.extensions import db


@pytest.fixture()
def app():
    application = create_app(TestingConfig)
    yield application
    with application.app_context():
        db.session.remove()
        db.drop_all()


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def auth_headers(client):
    response = client.post(
        "/api/v1/auth/login",
        json={"email": "demo@ctid.local", "password": "CTIDDemo!2026"},
    )
    payload = response.get_json()
    access_token = payload["data"]["access_token"]
    return {"Authorization": f"Bearer {access_token}"}
