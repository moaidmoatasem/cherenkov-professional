# Contributing to DAQIQ

Thank you for your interest in contributing to DAQIQ! This document provides guidelines for contributing to the project.

---

## 🎯 Project Status

**Current Phase**: Foundation (v0.1.x - Early Alpha)

We're building the basics right now. The project is **3 scanners** working toward **50+ scanners** by v1.0.

---

## 🤝 How to Contribute

### Types of Contributions Needed

1. **Scanner Development** (High Priority)
   - Implement new security checks
   - Improve existing scanners
   - Add test cases

2. **Test Coverage** (High Priority)
   - Unit tests for new features
   - Integration tests
   - Edge case testing

3. **Documentation** (Medium Priority)
   - API documentation
   - Tutorial content
   - Code comments

4. **Bug Fixes** (Always Welcome)
   - Security issues (see SECURITY.md for responsible disclosure)
   - Functional bugs
   - Performance improvements

5. **Code Review** (Ongoing)
   - Review open PRs
   - Security audits
   - Architecture feedback

---

## 🚀 Getting Started

### 1. Fork and Clone

```bash
# Fork on GitHub, then:
git clone https://github.com/YOUR_USERNAME/daqiq-professional.git
cd daqiq-professional
git remote add upstream https://github.com/moaidmoatasem/daqiq-professional.git
```

### 2. Set Up Development Environment

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in editable mode with dev dependencies
pip install -e .

# Install pre-commit hooks
pip install pre-commit
pre-commit install
```

### 3. Create a Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/issue-number-description
```

---

## 📝 Development Workflow

### Branch Naming

- `feature/scanner-sql-injection` - New features
- `fix/issue-42-xss-in-output` - Bug fixes
- `docs/api-reference` - Documentation
- `test/coverage-sanitizer` - Test improvements
- `refactor/cleanup-imports` - Code refactoring

### Commit Messages

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
type(scope): short description

Longer description if needed.

Fixes #123
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `test`: Tests
- `refactor`: Code refactoring
- `perf`: Performance improvement
- `chore`: Maintenance

**Examples:**
```
feat(scanner): add SQL injection detection

Implements basic SQL injection scanner with 10 common patterns.
Includes unit tests and integration with CLI.

Fixes #42
```

```
fix(security): prevent XSS in scan results

Escape HTML in JavaScript displayResults function.
Addresses OWASP XSS vulnerability.

CVSS: 7.5 (High)
```

### Code Style

We use automated tools (enforced by pre-commit):

```bash
# Format code
ruff format .

# Lint code
ruff check .

# Security checks
bandit -r daqiq/

# Type checks (if applicable)
mypy daqiq/
```

**Standards:**
- Python 3.10+ syntax
- Type hints encouraged
- Docstrings for public functions (Google style)
- Max line length: 100 characters
- No bare `except:` - use specific exceptions

---

## 🧪 Testing

### Running Tests

```bash
# All tests
pytest

# With coverage
pytest --cov=daqiq --cov-report=html

# Specific test file
pytest tests/unit/test_sanitizer.py

# Specific test
pytest tests/unit/test_sanitizer.py::test_redact_api_key -v
```

### Writing Tests

```python
# tests/unit/test_new_scanner.py
import pytest
from daqiq.scanners.new_scanner import NewScanner

class TestNewScanner:
    def test_basic_detection(self):
        """Test scanner detects basic vulnerability"""
        scanner = NewScanner("https://example.com")
        result = scanner.scan()
        assert result.vulnerabilities_found > 0

    def test_safe_target(self):
        """Test scanner returns clean for safe target"""
        scanner = NewScanner("https://safe-site.com")
        result = scanner.scan()
        assert result.is_safe
```

**Test Requirements:**
- Every new feature needs tests
- Aim for 80%+ coverage on new code
- Include edge cases and error handling
- Mock external dependencies (no real network calls in unit tests)

---

## 📋 Pull Request Process

### Before Submitting

- [ ] Code passes all pre-commit hooks
- [ ] Tests added for new features
- [ ] All tests pass (`pytest`)
- [ ] Coverage doesn't decrease
- [ ] Documentation updated (if applicable)
- [ ] CHANGELOG.md entry added (for features/fixes)
- [ ] Security implications considered

### PR Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation

## Testing
How was this tested?

## Checklist
- [ ] Tests pass
- [ ] Code linted
- [ ] Documentation updated
- [ ] CHANGELOG updated

Fixes #(issue number)
```

### Review Process

1. Automated checks must pass (ruff, bandit, pytest)
2. At least one maintainer review required
3. All review comments addressed
4. Squash commits before merge (maintainer will do this)

---

## 🐛 Reporting Bugs

### Before Reporting

- Search existing issues
- Try latest version
- Verify it's reproducible

### Bug Report Template

```markdown
**Description**
Clear description of the bug

**To Reproduce**
1. Run command X
2. With config Y
3. See error Z

**Expected Behavior**
What should happen

**Actual Behavior**
What actually happened

**Environment**
- OS: [e.g., Ubuntu 22.04]
- Python: [e.g., 3.10.5]
- DAQIQ: [e.g., v0.1.1]

**Logs**
```
Paste relevant logs
```
```

---

## 🔒 Security Vulnerabilities

**DO NOT** open public issues for security vulnerabilities.

See [SECURITY.md](SECURITY.md) for responsible disclosure process.

---

## 💡 Feature Requests

We welcome feature ideas! Please:

1. Check existing issues/discussions
2. Open a GitHub Discussion for large features
3. For small features, open an issue with `enhancement` label

**Template:**
```markdown
**Problem**
What problem does this solve?

**Proposed Solution**
How should it work?

**Alternatives**
Other approaches considered?

**Priority**
Why is this important now?
```

---

## 📚 Documentation

### Documenting Code

```python
def scan_target(url: str, timeout: int = 30) -> ScanResult:
    """Scan a target URL for vulnerabilities.

    Args:
        url: Target URL (http:// or https://)
        timeout: Request timeout in seconds (default: 30)

    Returns:
        ScanResult object with findings

    Raises:
        ValueError: If URL format is invalid
        TimeoutError: If scan exceeds timeout

    Example:
        >>> result = scan_target("https://example.com")
        >>> print(result.vulnerabilities_found)
        3
    """
```

### Documentation Files

- **README.md** - Quick start, features, installation
- **docs/api.md** - API reference
- **docs/architecture.md** - System design
- **CONTRIBUTING.md** - This file
- **SECURITY.md** - Security policy

---

## 🎯 Good First Issues

Look for issues labeled `good first issue`:

https://github.com/moaidmoatasem/daqiq-professional/labels/good%20first%20issue

These are beginner-friendly and well-documented.

---

## 🤔 Questions?

- **General questions**: [GitHub Discussions](https://github.com/moaidmoatasem/daqiq-professional/discussions)
- **Bug reports**: [GitHub Issues](https://github.com/moaidmoatasem/daqiq-professional/issues)
- **Security**: See [SECURITY.md](SECURITY.md)

---

## 📜 Code of Conduct

Be respectful, constructive, and professional. We're all here to build better security tools.

---

## 🙏 Recognition

Contributors are recognized in:
- CHANGELOG.md for their contributions
- README.md acknowledgments section
- Git commit history

Thank you for helping make DAQIQ better! 🚀
