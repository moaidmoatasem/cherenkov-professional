import asyncio
import time
import pytest
from typing import List

from cherenkov.core.engine import ScanEngine
from cherenkov.core.base_scanner import BaseScanner, ScanResult

class DummyRegistry:
    def __init__(self, scanners):
        self.scanners = scanners

    def list_scanners(self) -> List[str]:
        return list(self.scanners.keys())

    def get_scanner(self, name: str):
        return self.scanners[name]

class SlowScanner(BaseScanner):
    async def scan(self, target: str, timeout: float = 10.0) -> ScanResult:
        # Sleep slightly to test parallel execution
        await asyncio.sleep(0.5)
        return ScanResult(
            target=target,
            scanner_name=self.name,
            status="completed",
            findings=[],
        )

class TimeoutScanner(BaseScanner):
    async def scan(self, target: str, timeout: float = 10.0) -> ScanResult:
        # Sleep longer than the timeout
        await asyncio.sleep(timeout + 2.0)
        return ScanResult(
            target=target,
            scanner_name=self.name,
            status="completed",
            findings=[],
        )

class ErrorScanner(BaseScanner):
    async def scan(self, target: str, timeout: float = 10.0) -> ScanResult:
        raise ValueError("Intentional exception from ErrorScanner")

@pytest.mark.asyncio
async def test_scan_all_runs_in_parallel():
    # Setup 3 slow scanners, each taking 0.5s.
    # If sequential, total time would be ~1.5s.
    # If parallel, total time should be ~0.5s (slightly more).

    scanners = {
        "Slow1": SlowScanner,
        "Slow2": SlowScanner,
        "Slow3": SlowScanner,
    }
    registry = DummyRegistry(scanners)
    engine = ScanEngine(registry)

    start_time = time.time()
    results = await engine.scan_all("http://example.com")
    duration = time.time() - start_time

    assert len(results) == 3
    assert all(r.status == "completed" for r in results.values())
    assert duration < 1.0, f"Expected parallel execution < 1.0s, took {duration}s"

@pytest.mark.asyncio
async def test_scan_all_per_scanner_timeout_and_error():
    scanners = {
        "Fast": SlowScanner,
        "Timeout": TimeoutScanner,
        "Error": ErrorScanner,
    }
    registry = DummyRegistry(scanners)
    engine = ScanEngine(registry)

    progress_events = []

    async def progress_cb(name, status, result):
        progress_events.append((name, status))

    start_time = time.time()
    # We set timeout to 1.0s, TimeoutScanner will exceed this.
    results = await engine.scan_all("http://example.com", timeout=1.0, progress_callback=progress_cb)
    duration = time.time() - start_time

    assert len(results) == 3

    assert results["Fast"].status == "completed"

    assert results["Timeout"].status == "failed"

    assert results["Error"].status == "failed"

    # Check that events were emitted
    event_names = [e[0] for e in progress_events]
    assert set(event_names) == {"Fast", "Timeout", "Error"}

    fast_status = next(e[1] for e in progress_events if e[0] == "Fast")
    assert fast_status == "completed"

    error_status = next(e[1] for e in progress_events if e[0] == "Error")
    assert error_status == "failed"
