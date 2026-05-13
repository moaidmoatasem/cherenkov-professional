"""Tests for the FastAPI /api/scan endpoint (replaces retired Flask cherenkov_web.py tests)."""

import sys
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "packages"))

from cherenkov.api.main import app  # noqa: E402

client = TestClient(app, raise_server_exceptions=False)


def test_run_scan_invalid_url_format():
    # IPv6 bracket not closed — urlparse raises ValueError
    response = client.post("/api/scan", json={"url": "http://[::1"})
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data


def test_run_scan_missing_body():
    response = client.post("/api/scan", json={})
    # Missing required field `url` → 422 Unprocessable Entity from Pydantic
    assert response.status_code == 422


def test_run_scan_missing_url():
    response = client.post("/api/scan", json={"other": "value"})
    assert response.status_code == 422


def test_run_scan_invalid_scheme():
    response = client.post("/api/scan", json={"url": "ftp://example.com"})
    assert response.status_code == 400
    data = response.json()
    assert "Only http/https" in data["detail"]


def test_run_scan_missing_hostname():
    response = client.post("/api/scan", json={"url": "http://"})
    assert response.status_code == 400
    data = response.json()
    assert "hostname" in data["detail"]


def test_run_scan_success():
    """Happy path: valid URL returns scan_id and vulnerabilities list."""
    mock_finding = MagicMock()
    mock_finding.title = "Test Finding"
    mock_finding.severity = MagicMock()
    mock_finding.severity.value = "medium"
    mock_finding.cwe = "CWE-79"
    mock_finding.description = "Test description"
    mock_finding.remediation = "Fix it"

    mock_result = MagicMock()
    mock_result.findings = [mock_finding]

    with (
        patch(
            "cherenkov.api.main.ScanEngine",
            autospec=True,
        ) as mock_engine,
        patch("cherenkov.api.main.ScannerRegistry", autospec=True),
        patch("cherenkov.api.main.init_db"),
        patch("cherenkov.api.main.save_scan"),
    ):
        instance = mock_engine.return_value
        instance.scan_all = AsyncMock(return_value={"test_scanner": mock_result})

        response = client.post("/api/scan", json={"url": "http://example.com"})

    assert response.status_code == 200
    data = response.json()
    assert "scan_id" in data
    assert "vulnerabilities" in data
    assert data["count"] == 1
