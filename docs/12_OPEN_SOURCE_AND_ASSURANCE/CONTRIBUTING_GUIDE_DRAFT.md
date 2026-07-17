# Contributing Guide (Draft)

[//]: # (Document ID: BERUNDA-OSS-002 | Status: DRAFT | Classification: PUBLIC)

---

## 1. How to Contribute

We welcome contributions to Project Berunda. This is a hackathon project, but the architecture is designed for long-term evolution.

## 2. Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/{your-username}/berunda.git`
3. Set up the development environment (see README.md)
4. Create a feature branch: `git checkout -b feature/your-feature-name`
5. Make changes, write tests, commit
6. Submit a pull request to the `main` branch

## 3. Development Workflow

### 3.1 Code Style

| Language | Style Guide | Linter |
|----------|-------------|--------|
| Python | PEP 8 | Ruff |
| JavaScript/JSX | Airbnb + Prettier | ESLint |
| SQL | Consistent formatting (no trailing commas, uppercase keywords) | sqlfluff |

### 3.2 Testing

- All new code must include tests
- Unit tests: pytest (Python), Jest (JS)
- Integration tests: pytest with requests
- Security tests: pytest (custom RBAC/auth tests)
- Run the full test suite before committing: `pytest tests/ -v`

### 3.3 Commit Messages

Follow conventional commits:

```
feat: add entity resolution phonetic matching
fix: correct threshold calculation in ER scoring
docs: update API endpoint documentation
test: add entity resolution unit tests
chore: update dependency versions
```

### 3.4 Pull Request Process

1. Ensure all CI checks pass (lint, unit tests, integration tests)
2. Update documentation if adding or changing features
3. Update the planted test data manifest if adding new test cases
4. Request review from at least one team member
5. Squash merge to `main`

## 4. Code of Conduct

All contributors must abide by our Code of Conduct (see CODE_OF_CONDUCT.md).

## 5. Questions

Open a GitHub Discussion or contact the team via the hackathon channel.
