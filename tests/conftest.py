import copy

import pytest
from fastapi.testclient import TestClient

from src.app import activities, app

BASELINE_ACTIVITIES = copy.deepcopy(activities)


@pytest.fixture(autouse=True)
def reset_activities_state():
    """Reset in-memory activity data before and after each test."""
    activities.clear()
    activities.update(copy.deepcopy(BASELINE_ACTIVITIES))
    yield
    activities.clear()
    activities.update(copy.deepcopy(BASELINE_ACTIVITIES))


@pytest.fixture
def client():
    """Provide a FastAPI TestClient for endpoint testing."""
    return TestClient(app)
