from unittest.mock import AsyncMock, MagicMock, patch

import httpx
import pytest
from cherenkov.core.base_scanner import Severity
from cherenkov.scanners.path_traversal_scanner import PathTraversalScanner


@pytest.mark.asyncio
async def test_path_traversal_positive():
    scanner = PathTraversalScanner()
    target = "http://example.com/api"

    with patch(
        "httpx.AsyncClient.get",
        new_callable=AsyncMock,
        return_value=MagicMock(status_code=200, text="root:x:0:0:root:/root:/bin/bash"),
    ):
        result = await scanner.scan(target)

    assert result.target == target
    assert len(result.findings) == 1
    assert result.findings[0].severity == Severity.HIGH
    assert "Path Traversal" in result.findings[0].title


@pytest.mark.asyncio
async def test_path_traversal_negative():
    scanner = PathTraversalScanner()
    target = "http://example.com/api"

    with patch(
        "httpx.AsyncClient.get",
        new_callable=AsyncMock,
        return_value=MagicMock(status_code=404, text="Not Found"),
    ):
        result = await scanner.scan(target)

    assert len(result.findings) == 0
