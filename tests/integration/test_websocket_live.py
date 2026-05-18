import json
from unittest.mock import patch

import pytest
from cherenkov.api.main import app
from fastapi.testclient import TestClient


def test_websocket_live(monkeypatch):
    # To prevent TestClient from hanging forever due to the infinite while True loop
    # and the asyncio.sleep(5), we can mock asyncio.sleep to raise an exception or
    # simply use monkeypatch to break the loop or let it close when exiting the with block.
    # Actually, TestClient handles websocket disconnects reasonably well if we just exit the context.
    import asyncio

    # Let's mock asyncio.sleep so the test runs instantly and we don't wait 5 seconds.
    async def mock_sleep(*args, **kwargs):
        pass

    monkeypatch.setattr(asyncio, "sleep", mock_sleep)

    with TestClient(app) as client:
        with client.websocket_connect("/ws/live") as websocket:
            data1 = websocket.receive_json()
            assert data1["event"] == "health_pulse"

            data2 = websocket.receive_json()
            assert data2["event"] == "health_pulse"

            websocket.send_json({"command": "subscribe_scan", "scan_id": "test-123"})
            websocket.send_json({"command": "unsubscribe_scan", "scan_id": "test-123"})
