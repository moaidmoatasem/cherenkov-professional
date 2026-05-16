import pytest
from cherenkov.scanners.mobile.ios_scanner import IOSScanner
from cherenkov.core.base_scanner import Severity

@pytest.mark.asyncio
async def test_ios_scanner_findings():
    scanner = IOSScanner()
    result = await scanner.scan("test.ipa")
    
    assert result.scanner_name == "ios"
    assert len(result.findings) == 2
    
    ats_finding = next(f for f in result.findings if "ATS" in f.title)
    assert ats_finding.severity == Severity.HIGH
    assert ats_finding.cwe == "CWE-319"
    
    secret_finding = next(f for f in result.findings if "Secret" in f.title)
    assert secret_finding.severity == Severity.MEDIUM
    assert secret_finding.cwe == "CWE-798"
