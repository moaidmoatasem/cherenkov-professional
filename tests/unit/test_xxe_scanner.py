from unittest.mock import AsyncMock, MagicMock, patch

import httpx
import pytest
from cherenkov.core.base_scanner import Severity
from cherenkov.scanners.xxe_scanner import XXEScanner


@pytest.mark.asyncio
async def test_xxe_scanner_positive():
    scanner = XXEScanner()
    target = "http://example.com/api"

    with patch(
        "httpx.AsyncClient.post",
        new_callable=AsyncMock,
        return_value=MagicMock(status_code=200, text="root:x:0:0:root:/root:/bin/bash"),
    ):
        result = await scanner.scan(target)

    assert result.target == target
    assert len(result.findings) == 1
    assert result.findings[0].severity == Severity.HIGH
    assert "XXE" in result.findings[0].title


@pytest.mark.asyncio
async def test_xxe_scanner_negative():
    scanner = XXEScanner()
    target = "http://example.com/api"

    with patch(
        "httpx.AsyncClient.post",
        new_callable=AsyncMock,
        return_value=MagicMock(status_code=200, text="OK"),
    ):
        result = await scanner.scan(target)

    assert len(result.findings) == 0


@pytest.mark.asyncio
async def test_xxe_scanner_timeout():
    scanner = XXEScanner()
    target = "http://example.com/api"

    with patch("httpx.AsyncClient.post", side_effect=httpx.TimeoutException("Timeout")):
        result = await scanner.scan(target)

    assert len(result.findings) == 0
    assert result.status == "completed"
