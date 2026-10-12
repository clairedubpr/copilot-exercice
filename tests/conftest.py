import pytest
from fastapi.testclient import TestClient

import src.app as app_module


@pytest.fixture
def client(monkeypatch):
    test_activities = {
        "Chess Club": {
            "description": "Practice chess",
            "schedule": "Fridays",
            "max_participants": 12,
            "participants": ["student@mergington.edu"],
        },
        "Art Club": {
            "description": "Make art",
            "schedule": "Wednesdays",
            "max_participants": 18,
            "participants": [],
        },
    }
    monkeypatch.setattr(app_module, "activities", test_activities)

    with TestClient(app_module.app) as test_client:
        yield test_client