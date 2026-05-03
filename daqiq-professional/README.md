# 🛡️ DAQIQ - Local AI Security Framework

![Version](https://img.shields.io/badge/version-v0.1.1--alpha-blue)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![Tests](https://img.shields.io/badge/tests-passing-green)
![Coverage](https://img.shields.io/badge/coverage-30%25-yellow)
![License](https://img.shields.io/badge/license-MIT-green)

**Status**: 🚧 Early Alpha - Foundation Phase

Local-first security scanning framework with AI integration. Built for developers who want privacy-respecting security tools.

---

## 🎯 What Actually Works Today (v0.1.1)

### ✅ Core Features
- **3 working security scanners**:
  - HTTP security headers (5 checks)
  - HTTP methods detection (OPTIONS, PUT, DELETE, TRACE)
  - HTTPS/HTTP validation
- **Web interface**: Flask dashboard for running scans
- **CLI tool**: Basic command-line scanner
- **Local AI integration**: Ollama support (tinyllama model)
- **60 unit tests**: 30% code coverage

### 🔐 Security Features (v0.1.1)
- ✅ XSS protection in web interface
- ✅ Debug mode disabled by default
- ✅ URL validation and sanitization
- ✅ Localhost-only binding (configurable)
- ✅ Input validation on all endpoints

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10 or higher
- 2GB RAM minimum
- (Optional) Ollama for AI features

### Installation

```bash
# Clone repository
git clone https://github.com/moaidmoatasem/daqiq-professional.git
cd daqiq-professional

# Install dependencies
pip install -e .

# Run basic scan
python -m daqiq.cli scan https://example.com

# Or start web interface
python daqiq_web.py
# Open http://localhost:5000
```

### Docker (Coming Soon)
Docker support is planned for v0.2.0

---

## 📊 Honest Metrics

| Metric | Current | Target |
|--------|---------|--------|
| Working Scanners | 3 | 50+ by v1.0 |
| Test Coverage | 30% | 80% by v1.0 |
| Lines of Code | ~1,500 | - |
| Development Time | ~10 hours | - |
| Contributors | 1 | Open to PRs! |

---

## 🗺️ Roadmap

### v0.1.1 (Current) - Security Patch
- ✅ Fix critical security vulnerabilities
- ✅ Add SECURITY.md policy
- ✅ Align documentation with reality

### v0.2.0 (Week 2) - Foundation Complete
- 🔄 Enhanced PII detection
- 🔄 Structured logging
- 🔄 50% test coverage
- 📋 CONTRIBUTING.md
- 📋 CI/CD pipeline

### v0.3.0 (Month 1) - Scanner Expansion
- 📋 20 working scanners
- 📋 60% test coverage
- 📋 Docker support
- 📋 API documentation

### v1.0.0 (Month 6) - Production Ready
- 📋 50+ scanners
- 📋 80% test coverage
- 📋 CrewAI multi-agent orchestration
- 📋 Comprehensive documentation
- 📋 Security audit complete

**Legend**: ✅ Complete | 🔄 In Progress | 📋 Planned

---

## 🔧 Configuration

Create `.env` file (optional):

```env
# Flask web interface
FLASK_DEBUG=false           # Never true in production!
FLASK_HOST=127.0.0.1        # Localhost only (use 0.0.0.0 to expose)
FLASK_PORT=5000

# Ollama AI (optional)
OLLAMA_MODEL=tinyllama      # Fast, low-RAM model
OLLAMA_HOST=http://localhost:11434

# Scanning options
ALLOW_LOCALHOST_SCAN=false  # Enable to scan localhost URLs
```

---

## 🛡️ Security

**v0.1.1 fixes critical vulnerabilities from v0.1.0:**
- Remote Code Execution via Flask debug mode (CVSS 9.8) ✅ Fixed
- Stored XSS in web interface (CVSS 7.5) ✅ Fixed  
- Silent exception handling causing false negatives (CVSS 5.0) ✅ Fixed

**See [SECURITY.md](SECURITY.md) for:**
- Vulnerability disclosure policy
- Security best practices
- Contact information

**⚠️ Important**: This is an early-stage security tool. Do not use for production security assessments yet. Only scan targets you own or have permission to test.

---

## 🤝 Contributing

Contributions welcome! This is an early-stage project that needs:

- [ ] More scanner implementations
- [ ] Test coverage improvements
- [ ] Documentation
- [ ] Bug reports and fixes
- [ ] Security reviews

**How to contribute:**
1. Fork the repository
2. Create a feature branch
3. Add tests for your changes
4. Submit a pull request

See [CONTRIBUTING.md](CONTRIBUTING.md) (coming soon)

---

## 📖 Documentation

- [Installation Guide](docs/installation.md) (coming soon)
- [API Reference](docs/api.md) (coming soon)
- [Architecture](docs/architecture.md) (coming soon)

---

## 🎯 Project Vision (Long-term)

DAQIQ aims to become a comprehensive local-first security framework with:
- 100+ automated security scanners
- AI-powered vulnerability detection
- Multi-agent orchestration (CrewAI)
- Zero-cloud-dependency architecture
- PII redaction and secret detection
- Autonomous code generation for new scanners

**Current status**: Foundation phase. We're building the basics right first.

---

## 📊 AI Model Benchmarks

| Model | Speed | RAM | Status |
|-------|-------|-----|--------|
| tinyllama | 8.47s | 637MB | ✅ Default |
| qwen2.5-coder:3b | 97.98s | 2.1GB | ⚠️ Slow |
| Larger models | >120s | >4GB | ❌ Not recommended |

**Note**: AI features are optional. Core scanners work without AI.

---

## 📄 License

MIT License - See [LICENSE](LICENSE)

---

## 🙏 Acknowledgments

- Security review feedback from the community
- CrewAI framework for multi-agent architecture inspiration
- Ollama for local LLM infrastructure

---

## 📞 Contact

- **Issues**: [GitHub Issues](https://github.com/moaidmoatasem/daqiq-professional/issues)
- **Security**: See [SECURITY.md](SECURITY.md)
- **Discussions**: [GitHub Discussions](https://github.com/moaidmoatasem/daqiq-professional/discussions)

---

## ⚠️ Disclaimer

This is an alpha-stage security tool under active development. Use at your own risk. Always:
- Test on authorized targets only
- Verify scan results manually
- Keep dependencies updated
- Review SECURITY.md before deployment

**Not recommended for production security assessments yet.**

---

**Built with ❤️ for security-conscious developers who value privacy**
