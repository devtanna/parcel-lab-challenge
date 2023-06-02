import logging

import pytest
import requests

logger = logging.getLogger(__name__)

class MockResponse:
    def __init__(self, json_data=None, status_code=200):
        self.json_data = json_data
        self.status_code = status_code

    def json(self):
        return self.json_data

@pytest.fixture
def mock_requests_get(monkeypatch):
    def mock_get(*args, **kwargs):
        return MockResponse({
            "weather": [{"icon": "01d"}],
            "main": {
                "temp": 20,
                "feels_like": 18,
                "temp_min": 15,
                "temp_max": 25,
            }
        }, status_code=200)

    monkeypatch.setattr(requests, "get", mock_get)