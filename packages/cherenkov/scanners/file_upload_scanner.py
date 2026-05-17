"""File Upload Scanner — detects unrestricted file upload endpoints."""

import logging

from cherenkov.core.base_scanner import BaseScanner, Finding, ScanResult, Severity

logger = logging.getLogger(__name__)


class FileUploadScanner(BaseScanner):
    """Checks for unrestricted file upload vectors (CWE-434)."""

    cwe = "CWE-434"

    async def scan(self, target: str, timeout: float = 10.0) -> ScanResult:
        findings: list[Finding] = []
        try:
            import httpx

            upload_paths = ["/upload", "/file/upload", "/api/upload", "/admin/upload"]
            async with httpx.AsyncClient(timeout=timeout, verify=True) as client:
                for path in upload_paths:
                    url = target.rstrip("/") + path
                    try:
                        r = await client.post(
                            url,
                            files={"file": ("chk_probe.php", b"<?php echo 1; ?>", "application/octet-stream")},
                        )
                        if r.status_code not in (404, 405, 403, 401, 301, 302):
                            findings.append(
                                Finding(
                                    title="Possible Unrestricted File Upload",
                                    severity=Severity.HIGH,
                                    description=f"Upload endpoint {url} responded with HTTP {r.status_code}. Validate MIME type and extension enforcement.",
                                    cwe=self.cwe,
                                    remediation="Enforce MIME-type allowlist server-side, randomise stored filenames, store outside webroot.",
                                )
                            )
                    except httpx.HTTPError as exc:
                        logger.debug("Upload probe %s unreachable: %s", url, exc)
        except ImportError as exc:
            logger.warning("FileUploadScanner unavailable: %s", exc)
        return ScanResult(target=target, scanner_name=self.name, findings=findings)
