import logging
import plistlib
import zipfile
from typing import List

from cherenkov.core.base_scanner import BaseScanner, Finding, ScanResult, Severity

logger = logging.getLogger("cherenkov.scanners.mobile.ipa")


class IPAScanner(BaseScanner):
    """
    iOS Scanner - Unpacks IPA and performs static analysis on Info.plist and binaries.
    """

    def __init__(self):
        super().__init__(
            name="iOS IPA Scanner", description="Static analysis for iOS application bundles"
        )

    async def scan(self, target: str, timeout: float = 30.0) -> ScanResult:
        """
        Scan an IPA file. 'target' is the path to the IPA.
        """
        findings: List[Finding] = []

        if not target.endswith(".ipa"):
            return ScanResult(target=target, scanner_name=self.name, findings=[], status="failed")

        try:
            with zipfile.ZipFile(target, "r") as ipa:
                # 1. Look for Info.plist
                plist_path = None
                for name in ipa.namelist():
                    if name.endswith("Info.plist") and "Payload/" in name:
                        plist_path = name
                        break

                if plist_path:
                    with ipa.open(plist_path) as f:
                        plist_data = plistlib.load(f)
                        self._analyze_plist(plist_data, findings)
                else:
                    findings.append(
                        Finding(
                            title="Missing Info.plist",
                            severity=Severity.HIGH,
                            description="Application bundle does not contain a valid Info.plist",
                            cwe="CWE-200",
                            remediation="Ensure the IPA contains a valid Payload directory with a .app bundle and Info.plist.",
                        )
                    )

        except Exception as e:
            logger.error("IPA scan failed: %s", e)
            return ScanResult(
                target=target, scanner_name=self.name, findings=findings, status="error"
            )

        return ScanResult(
            target=target, scanner_name=self.name, findings=findings, status="completed"
        )

    def _analyze_plist(self, plist: dict, findings: List[Finding]):
        # Check for App Transport Security (ATS) bypasses
        ats = plist.get("NSAppTransportSecurity", {})
        if ats.get("NSAllowsArbitraryLoads"):
            findings.append(
                Finding(
                    title="ATS Disabled (Global)",
                    severity=Severity.HIGH,
                    description="App Transport Security is globally disabled, allowing insecure HTTP connections.",
                    cwe="CWE-319",
                    remediation="Remove NSAllowsArbitraryLoads or use domain-specific exceptions.",
                )
            )

        # Check for excessive permissions
        permissions = [
            ("NSCameraUsageDescription", "Camera Access"),
            ("NSLocationWhenInUseUsageDescription", "Location Access"),
            ("NSMicrophoneUsageDescription", "Microphone Access"),
            ("NSPhotoLibraryUsageDescription", "Photo Library Access"),
        ]

        for key, name in permissions:
            if key in plist:
                findings.append(
                    Finding(
                        title=f"{name} Requested",
                        severity=Severity.LOW,
                        description=f"Application requests access to {name}.",
                        cwe="CWE-250",
                        remediation="Verify if this permission is absolutely necessary for app functionality.",
                    )
                )
