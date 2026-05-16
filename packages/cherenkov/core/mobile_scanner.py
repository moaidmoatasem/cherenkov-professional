"""Base Mobile Scanner"""

from abc import abstractmethod
from typing import List

from cherenkov.core.base_scanner import BaseScanner, Finding, ScanResult


class MobileScanner(BaseScanner):
    """Abstract base class for Mobile Scanners (Android/iOS)"""

    def __init__(self, name: str, description: str):
        super().__init__(name, description)

    @abstractmethod
    async def scan_file(self, file_path: str) -> List[Finding]:
        """Scan a mobile binary (APK/IPA)"""
        pass

    async def scan(self, target: str, timeout: float = 30.0) -> ScanResult:
        """Standard scan implementation for mobile"""
        import time

        start = time.monotonic()
        # In a real scenario, we might download the file first if target is a URL
        # For now, we assume target is a path or we simulate the analysis
        findings = await self.scan_file(target)

        return ScanResult(
            target=target,
            scanner_name=self.name,
            findings=findings,
            duration_ms=(time.monotonic() - start) * 1000,
        )
