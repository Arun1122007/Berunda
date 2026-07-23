# Changelog

All notable changes to Project Berunda are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [0.1.0] — 2026-07-18

### Added

- **Enterprise repository restructuring**: Complete re-organization from flat design repo to production-ready monorepo structure:
  - `apps/` — Application scaffolding (web frontend, Catalyst API functions, background worker)
  - `src/` — Source code scaffolding (AI, ML, pipelines, shared utilities)
  - `tests/` — Layered test structure (unit, integration, e2e, performance, security)
  - `config/` — Environment-aware configuration (base, dev, test, staging, production)
  - `infrastructure/` — Docker, Catalyst config, environment templates
  - `.github/` — CI/CD workflows, issue/PR templates, Dependabot, CODEOWNERS
  - `security/` — Security policies, scanning, threat models
  - `monitoring/` — Dashboards, alerts, logging, tracing

- **Root-level enterprise files**:
  - `.editorconfig`, `.gitattributes`, `.dockerignore`, `.pre-commit-config.yaml`
  - `.env.example` with documented environment variables
  - `LICENSE` (MIT), `CHANGELOG.md`, `SECURITY.md`, `CODE_OF_CONDUCT.md`, `CONTRIBUTING.md`
  - `berunda.ps1` (PowerShell build orchestration)
  - `docker-compose.yml` (full local dev stack)
  - `package.json` (root workspace), `requirements.txt`

- **Documentation reorganization**:
  - `docs/` directories renamed from numbered prefixes to descriptive kebab-case
  - `docs/99_REPORTS/` promoted to root-level `reports/`
  - `pdf_extracted.md` moved to `docs/reference/`
  - Cross-reference paths updated across all documents

### Changed

- Documentation directory structure: numbered prefixes removed in favor of descriptive names
- README.md updated with comprehensive project documentation
- `.gitignore` extended for new directory structure

### Preserved

- All existing documentation (79 files) — content unchanged, only paths updated
- All manifest files (9 files) — unchanged
- All source blueprint documents in `blueprints/h2s/` — kept in place with README
- All agent instructions (AGENTS.md) — preserved

---

## [0.0.1] — 2026-07-17

### Added

- Initial project scaffold with design documentation baseline
- 12 source blueprint documents in `blueprints/h2s/`
- 79 documentation files across 14 categories
- PowerShell acquisition preflight script
- Resource manifest and provenance tracking
- Directory structure for data, models, boundaries, quarantine
