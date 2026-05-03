# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 0.1.1   | :white_check_mark: |
| 0.1.0   | :x: (Critical vulnerabilities) |

## Security Updates in v0.1.1

### Critical Vulnerabilities Fixed

#### 1. Remote Code Execution via Flask Debug Mode (CVSS 9.8)
- **Issue**: Flask debug mode enabled on all network interfaces (`0.0.0.0`)
- **Impact**: Arbitrary code execution via Werkzeug debugger
- **Fix**: Debug mode disabled by default, localhost-only binding
- **File**: `daqiq_web.py`

#### 2. Stored Cross-Site Scripting (XSS) (CVSS 7.5)
- **Issue**: User input concatenated directly into HTML without escaping
- **Impact**: Script injection via malicious target URLs
- **Fix**: HTML escaping function added
- **File**: `daqiq_web.py` line 169

#### 3. Silent Exception Handling (CVSS 5.0)
- **Issue**: Bare `except:` blocks causing false negatives
- **Impact**: Security scanner reports "safe" when scan failed
- **Fix**: Specific exception handling with proper error reporting
- **File**: `daqiq_simple_scanner.py` line 72

### Additional Security Improvements

- URL validation added (scheme, format, localhost protection)
- Environment-based configuration for debug mode
- Warnings displayed when running in insecure configurations

## Reporting a Vulnerability

**DO NOT** open public issues for security vulnerabilities.

Email: moaid.moatasem@example.com (replace with actual email)

Include:
- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if available)

We aim to respond within 48 hours and provide a fix within 7 days for critical issues.

## Security Best Practices

When running DAQIQ:

1. **Never** set `FLASK_DEBUG=true` in production
2. **Never** bind to `0.0.0.0` on untrusted networks
3. Use environment variables for configuration
4. Keep dependencies updated
5. Run scans only against authorized targets
6. Review scan reports for false negatives

## Acknowledgments

Thanks to the security researchers who identified these vulnerabilities during code review.
