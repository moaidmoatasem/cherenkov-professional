import pytest
import json
import asyncio
from unittest.mock import patch
from fastapi.testclient import TestClient
from starlette.websockets import WebSocketDisconnect
from cherenkov.api.main import app

def test_websocket_live(monkeypatch):
    import cherenkov.api.main as main_module

    # We don't want the real background loop to keep going forever and blocking TestClient exit
    # TestClient doesn't cancel background tasks immediately if they are created with asyncio.create_task and don't exit.

    # Mock asyncio.sleep to raise WebSocketDisconnect after 2 iterations
    sleep_call_count = 0

    async def mock_sleep(*args, **kwargs):
        nonlocal sleep_call_count
        sleep_call_count += 1
        if sleep_call_count >= 3:
            raise WebSocketDisconnect()
        return

    monkeypatch.setattr(main_module.asyncio, "sleep", mock_sleep)

    with TestClient(app) as client:
        with client.websocket_connect("/ws/live") as websocket:
            data1 = websocket.receive_json()
            assert data1["event"] == "health_pulse"

            data2 = websocket.receive_json()
            assert data2["event"] == "health_pulse"

            websocket.send_json({"command": "subscribe_scan", "scan_id": "test-123"})
            websocket.send_json({"command": "unsubscribe_scan", "scan_id": "test-123"})
