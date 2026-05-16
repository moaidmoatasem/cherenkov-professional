import pytest
import zipfile
import plistlib
import os
import tempfile
from cherenkov.scanners.mobile.ipa_scanner import IPAScanner

@pytest.fixture
def mock_ipa():
    with tempfile.NamedTemporaryFile(suffix=".ipa", delete=False) as tmp:
        with zipfile.ZipFile(tmp, 'w') as zf:
            plist = {
                "NSAppTransportSecurity": {"NSAllowsArbitraryLoads": True},
                "NSCameraUsageDescription": "We need your camera"
            }
            zf.writestr("Payload/TestApp.app/Info.plist", plistlib.dumps(plist))
        return tmp.name

@pytest.mark.asyncio
async def test_ipa_scanner_analysis(mock_ipa):
    scanner = IPAScanner()
    result = await scanner.scan(mock_ipa)
    
    assert result.status == "completed"
    assert len(result.findings) >= 2
    
    titles = [f.title for f in result.findings]
    assert "ATS Disabled (Global)" in titles
    assert "Camera Access Requested" in titles
    
    os.remove(mock_ipa)

@pytest.mark.asyncio
async def test_ipa_scanner_invalid_file():
    scanner = IPAScanner()
    result = await scanner.scan("not_an_ipa.txt")
    assert result.status == "failed"
    assert len(result.findings) == 0
