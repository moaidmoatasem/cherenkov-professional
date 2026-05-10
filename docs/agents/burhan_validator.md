# Burhan (البرهان) Stateless Validator

## Overview

Burhan is a lightweight, stateless PoC validation worker that verifies security findings using safe, non-destructive payload execution. It is designed for speed (<5s per validation) and zero external dependencies, running entirely on local hardware with an optional 1B/3B quantized Ollama model.

## Architecture

```
Finding + PoC Payload
        │
        ▼
  ┌─────────────┐
  │ Burhan       │  Stateless, no DB, no side effects
  │ Validator    │  LLM-backed (qwen2.5-coder:1.5b)
  └──────┬──────┘
         │
    ┌────┴────┐
    │ 5s T/O  │  Watchdog kills slow probes
    └────┬────┘
         │
   ┌─────┴──────┐
   │ SHA-256     │  Evidence hash
   │ Log File    │  JSON to logs/burhan/
   └─────┬──────┘
         │
         ▼
  BurhanResult { verdict, evidence_hash, log_path }
```

## Supported Vulnerability Types

| Type | Payloads | Detection Method |
|------|----------|------------------|
| XSS | `<script>alert(1)</script>`, `<img src=x onerror=alert(1)>` | Reflection check in response body |
| SQLi | `' OR '1'='1`, `' UNION SELECT 1--` | Error indicator detection (SQL syntax, mysql, odbc) |
| CSRF | Form autosubmit, img-based POST | Status code 200 on POST without token |

## Usage

```python
from cherenkov.agents.burhan_validator import BurhanValidator

validator = BurhanValidator()

target = "http://localhost:8080/search?q="
result = validator.validate(
    target=target,
    vuln_type="xss",
    finding_title="Reflected XSS in search",
)

print(result.verdict)         # valid / invalid / skipped / timeout
print(result.evidence_hash)   # SHA-256 hex digest
print(result.log_path)        # logs/burhan/xss_123456.json
```

## Safety Controls

- **5-second hard timeout** — all HTTP requests use `timeout=5`
- **Local targets only** — rejects targets not matching `localhost`, `127.0.0.1`, `0.0.0.0`, `::1`
- **Payload sanitization** — strips destructive patterns (`/etc/passwd`, `rm -rf`, etc.)
- **No subprocess execution** — all probes use HTTP/S only
- **No external egress** — DNS resolution limited to loopback

## Model Integration

Optional Ollama integration for intelligent verdict analysis:

```python
validator = BurhanValidator(model="qwen2.5-coder:1.5b")
if validator.model_available():
    # LLM-assisted validation
    pass
```

Requires [Ollama](https://ollama.ai) with a compatible 1B-3B model installed.

## Output Schema

```json
{
    "finding_title": "Reflected XSS in search",
    "vuln_type": "xss",
    "verdict": "valid",
    "evidence_hash": "sha256 hex...",
    "log_path": "logs/burhan/xss_1746812345.json",
    "duration_ms": 342.1,
    "detail": "XSS reflected in response"
}
```

## Log Files

All probes are logged to `logs/burhan/` as timestamped JSON files for audit trail and debugging.
