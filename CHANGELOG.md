# Changelog

All notable changes to Project Helix will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.1.0] - 2026-05-11

### Added
- **GStack-Fusion v0.7.0 Integration**: 27 skills migrated from GStack-Fusion
- **10 new skills** from agent-skills (5) and mattpocock/skills (5)
- Skills reorganized into 8 SDLC categories (planning, architecture, implementation, quality, debugging, process, deploy, security)

### Changed
- Skills migrated from `skill/` to `skills/` with SDLC category structure
- Helix unique skills (build, verify, gate, browse, learn, checkpoint) preserved
- bin/ and lib/ migrated from GStack-Fusion
- docs/ populated from GStack-Fusion

### Preserved
- 6 Helix-unique skills: helix-build, helix-verify, helix-gate, helix-browse, helix-learn, helix-checkpoint
- Original `skill/` directory backed up to `skill.bak/`

### Stats
- Total skills: 33 (up from 12)
- Sources: GStack-Fusion (27) + Helix (6)

---

## [1.0.0] - 2026-04-19

### Added
- IntentClassifier - Rule-based intent classification with context enhancement
- HelixOrchestrator v2 - Enhanced orchestration with IntentClassifier integration
- Type annotations - Full mypy type coverage for core/, skills/, adapters/
- Test coverage - 93% for core/, 62% for skills/

### Changed
- Skill routing via INTENT_TO_SKILL mapping
- HelixConfig with timeout_seconds support
- Improved error handling and confidence calculation

### Architecture
- Four-layer architecture: Infrastructure → Execution Engine → Quality Assurance → Meta-Methodology
- AI agent-agnostic design with pluggable adapters

---

## [1.0.0-beta.1] - 2026-04-11

### Added
- 12 Skills across 4 layers (Execution, Quality, Infrastructure, Meta)
- Core modules: orchestrator, context, intent recognition
- AI Engine Manager with load balancing and health checking
- Intent Recognition Engine with pattern matching
- Plugin System with SkillPlugin and AdapterPlugin
- REST API (FastAPI) for programmatic access
- CI/CD generators (GitHub Actions, GitLab CI)
- Webhook handlers for external integrations
- Performance monitoring with metrics collection
- Auto-documentation generator

### Changed
- Converted to Beta release cycle
- Status changed from "Stable" to "Beta 🧪"

### Architecture
- L1: Infrastructure - browse, design, learn, checkpoint
- L2: Execution Engine - spec, build, verify, ship
- L3: Quality Assurance - review, test, audit, gate
- L4: Meta-Methodology - orchestration, plugins

---

## [0.9.0] - 2026-04-10

### Added
- Production Ready module
- Performance monitoring (`monitoring/`)
- Auto-documentation generator (`docs/generator.py`)
- Health check endpoints

### Skills Added
- `verify` - Automated verification loop
- `ship` - Release and delivery

---

## [0.8.0] - 2026-04-10

### Added
- Platform Engineering layer
- REST API server (`api/server.py`)
- CI/CD configuration generators
- Webhook handlers

### Skills Added
- `test` - Intelligent testing
- `audit` - Security audit

---

## [0.7.0] - 2026-04-10

### Added
- AI Engine integration layer (`engines/`)
- AIEngineManager with:
  - Multi-engine support
  - Load balancing
  - Health checking
  - Automatic failover
- Intent Recognition Engine:
  - Pattern matching
  - Keyword detection
  - Learning capability

### Skills Added
- `review` - Code review

---

## [0.6.0] - 2026-04-09

### Added
- Infrastructure layer (L1)
- Native Helix skills (not integrated from external frameworks)

### Skills Added
- `browse` - Browser control for QA
- `design` - Design generation
- `learn` - Continuous learning
- `checkpoint` - State persistence

---

## [0.5.0] - 2026-04-09

### Added
- Quality Assurance layer
- Security audit capabilities
- Quality gate system

### Skills Added
- `audit` - Security audit (moved to L2 in v0.8.0)
- `gate` - Quality gate (moved to L2 in v0.8.0)

---

## [0.1.0] - 2026-04-09

### Added
- Initial project structure
- Core philosophy and vision
- Four methodologies integration:
  - Agile (Spec-driven)
  - DevOps (Verification loop)
  - Platform Engineering (Skills as services)
  - Harness Engineering (Human-AI collaboration)

### Skills Added
- `spec` - Requirement to specification
- `build` - Specification to code

---

## Release Schedule

See [BETA_RC_RELEASE_PLAN.md](docs/roadmap/BETA_RC_RELEASE_PLAN.md) for detailed release schedule.

```
v1.0.0-beta.1  ← Current (代码基础验证)
     ↓
v1.0.0-beta.2  ← 测试补齐 + 文档完善 (in progress)
     ↓
v1.0.0-beta.3  ← Docker支持 + 类型标注
     ↓
v1.0.0-rc.1    ← RC候选 (功能冻结)
     ↓
v1.0.0-rc.2    ← RC候选 (bug修复)
     ↓
v1.0.0-rc.3    ← RC候选 (最终验证)
     ↓
v1.0.0-STABLE  ← 正式发布
```

---

## Migration Guides

### Upgrading to v1.0.0-beta.x

This is a beta release. API may change before stable release.

### Upgrading from v0.x to v1.0.0

- All skill statuses updated to "Beta 🧪"
- Version scheme changed from v0.x to v1.0.0-beta.1

---

## Deprecated Features

None yet - this is the first beta release.

---

## Known Issues

- Unit test coverage is at 23% (target: 70% by v1.0.0-stable)
- Docker support coming in v1.0.0-beta.3
- Type annotations (mypy) coming in v1.0.0-beta.3

---

## Contributors

- Peter Cheng - Project Lead
- Jarvis - AI Assistant

---

*Generated: 2026-04-11*
