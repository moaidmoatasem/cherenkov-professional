import pytest
import json
from unittest.mock import patch
from fastapi.testclient import TestClient
from fastapi import WebSocketDisconnect
from cherenkov.api.main import app

@patch('cherenkov.api.main.asyncio.sleep', side_effect=WebSocketDisconnect)
def test_websocket_live(mock_sleep):
    with TestClient(app) as client:
        with client.websocket_connect("/ws/live") as websocket:
            data1 = websocket.receive_json()
            assert data1["event"] == "health_pulse"
