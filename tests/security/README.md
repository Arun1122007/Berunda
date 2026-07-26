# Security Tests

Automated security scanning and penetration tests.

- **SAST**: CodeQL (GitHub), Ruff (Python)
- **DAST**: OWASP ZAP (scheduled)
- **Dependency scanning**: pip-audit (Python), npm audit (Node)
- **Secrets detection**: TruffleHog
- **Container scanning**: Trivy
- **Run**: `pytest -m security -v` or via GitHub Actions `security-scan.yml`
