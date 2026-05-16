"""File Upload Scanner"""

import time
from typing import List

import httpx

from cherenkov.core.base_scanner import BaseScanner, Finding, ScanResult, Severity


class FileUploadScanner(BaseScanner):
    """Scanner to detect Unsafe File Upload vulnerabilities."""

    def __init__(self, name: str = "", description: str = ""):
        super().__init__(name, description)

    async def scan(self, target: str, timeout: float = 10.0) -> ScanResult:
        """Execute the scan - attempting to upload a suspicious file."""
        start_time = time.time()
        findings: List[Finding] = []

        # Use an obfuscated or safe payload to avoid AV triggers
        # Instead of a webshell, we just check if we can upload any executable type
        payload = "CHERENKOV_SECURITY_TEST_UPLOAD"
        files = {"file": ("test_upload.php", payload, "application/x-php")}

        try:
            async with httpx.AsyncClient(timeout=timeout, verify=True) as client:
                upload_url = target.rstrip("/") + "/upload"
                response = await client.post(upload_url, files=files, follow_redirects=True)

                if response.status_code in [200, 201] and (
                    "success" in response.text.lower() or "test_upload.php" in response.text
                ):
                    findings.append(
                        Finding(
                            title="Unsafe File Upload",
                            severity=Severity.HIGH,
                            description="The application allows uploading files with executable extensions (e.g. .php).",
                            cwe="CWE-434",
                            remediation="Implement strict file extension validation and store uploads outside the web root.",
                        )
                    )
        except (httpx.RequestError, httpx.TimeoutException):
            pass

        duration_ms = (time.time() - start_time) * 1000

        return ScanResult(
            target=target,
            scanner_name=self.name,
            findings=findings,
            duration_ms=duration_ms,
            status="completed",
        )
