# DAQIQ — Local AI Security Testing Framework

> **Alpha stage** • 3 working scanners • Built for security engineers who want AI-assisted testing without cloud dependencies

[![Security](https://img.shields.io/badge/security-v0.1.1--patched-green)](SECURITY.md)
[![Tests](https://img.shields.io/badge/coverage-30%25-yellow)]()
[![Python](https://img.shields.io/badge/python-3.10%2B-blue)]()

**Current Status:** 🚧 v0.1.1-alpha — Phase 1 of 6-month roadmap

---

## What Actually Works Today

✅ **3 HTTP Security Scanners**
- Security headers (X-Frame-Options, CSP, HSTS, etc.)
- HTTP methods (TRACE, PUT, DELETE testing)
- TLS/HTTPS validation

✅ **Basic Infrastructure**
- CLI: `daqiq scan <url>`
- Web dashboard (localhost-only, security hardened)
- Local Ollama integration (experimental scaffold)

✅ **Security Hardened**
- All critical vulnerabilities from v0.1.0 patched
- No debug mode, localhost binding only
- Input validation on all user-supplied data

---

## What Doesn't Work Yet

❌ CrewAI multi-agent orchestration (Phase 4 - Week 12)  
❌ 132 scanners (Phase 3 target: 50+)  
❌ PII redaction engine (not implemented)  
❌ Dual-brain architecture (Phase 4 - Week 14)  
❌ SARIF output (Phase 5 - Week 20)  

---

## Honest Metrics

| Metric | Current | Target (v1.0) |
|--------|---------|---------------|
| Working scanners | **3** | 50+ |
| Test coverage | **~30%** | 80% |
| Lines of code | **~1,500** | ~15,000 |
| Security validated | ✅ | ✅ |
| Production ready | ❌ | ✅ |

---

## Quick Start

```bash
# Clone
git clone https://github.com/moaidmoatasem/daqiq-professional
cd daqiq-professional

# Install
pip install -e .

# Run your first scan
daqiq scan https://example.com
```

### With Docker

```bash
docker build -t daqiq .
docker run --rm daqiq scan https://example.com
```

---

## Development Roadmap

**6-Month Plan to v1.0**

- [x] **Phase 0**: Critical security fixes *(Week 0)* ✅
- [ ] **Phase 1**: Repository cleanup *(Weeks 1-2)*
- [ ] **Phase 2**: Architecture overhaul *(Weeks 2-4)*
- [ ] **Phase 3**: 50+ validated scanners *(Weeks 4-10)*
- [ ] **Phase 4**: AI integration *(Weeks 10-18)*
- [ ] **Phase 5**: Production hardening *(Weeks 18-26)*

See [docs/ROADMAP.md](docs/ROADMAP.md) for details.

---

## Architecture (Planned - Phase 2)


---

## Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for:
- How to add a new scanner
- Testing requirements (DVWA validation)
- Code style guide

**Good first issues**: [Scanner requests](https://github.com/moaidmoatasem/daqiq-professional/labels/scanner-request)

---

## Security

**Vulnerability Disclosure**: See [SECURITY.md](SECURITY.md)

**Recent Patches**:
- v0.1.1-security: Fixed RCE, XSS, and exception handling vulnerabilities

---

## License

MIT License - see [LICENSE](LICENSE)

---

## Acknowledgments

Built with honesty. Inspired by the need for local-first security testing.

Not ready for production yet. Check back in 6 months for v1.0.
