# Helix

> AI Era Software Engineering Methodology - Human-AI Co-evolution Framework

[![Version](https://img.shields.io/badge/version-0.9.0-blue)](https://github.com/opensourceclaw/helix)
[![Python](https://img.shields.io/badge/python-3.10+-green)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-yellow)](LICENSE)

## Overview

Helix is an AI-powered software engineering methodology that enables human-AI co-evolution through a four-layer architecture:

- **L4**: Meta-Methodology (Methodology selection)
- **L3**: Execution Engine (Spec → Build → Verify → Ship)
- **L2**: Quality Assurance (Review → Test → Audit → Gate)
- **L1**: Infrastructure (Browse → Design → Learn → Checkpoint)

## Quick Start

```bash
# Install
pip install helix

# List skills
helix list-skills

# Run a skill
helix spec "Create a user authentication system"
helix build
helix verify
helix ship
```

## Installation

```bash
# Basic
pip install helix

# With API server
pip install helix[api]

# Development
git clone https://github.com/opensourceclaw/helix.git
cd helix
pip install -e .
```

## Skills

| Skill | Layer | Description |
|-------|-------|-------------|
| `/spec` | L3 | Requirement to specification |
| `/build` | L3 | Specification to code |
| `/verify` | L3 | Automated verification |
| `/ship` | L3 | Release & delivery |
| `/review` | L2 | Code review |
| `/test` | L2 | Intelligent testing |
| `/audit` | L2 | Security audit |
| `/gate` | L2 | Quality gate |
| `/browse` | L1 | Browser control |
| `/design` | L1 | Design generation |
| `/learn` | L1 | Continuous learning |
| `/checkpoint` | L1 | State persistence |

## Configuration

Helix looks for configuration in:
1. `./helix.yaml`
2. `./helix.json`
3. `~/.helix/config.yaml`

Example configuration:

```yaml
version: "0.9.0"

engines:
  claude:
    model: sonnet
    priority: 10

skills:
  gate:
    min_coverage: 70
    max_complexity: 10
```

## API Server

```bash
# Start API server
helix serve

# API docs at http://localhost:8080/docs
```

## CI/CD Integration

```bash
# Generate GitHub Actions
helix ci github

# Generate GitLab CI
helix ci gitlab
```

## Development

```bash
# Run tests
pytest

# Lint
ruff check src/

# Type check
mypy src/
```

## Documentation

- [Architecture](docs/ARCHITECTURE.md)
- [Skills Guide](docs/skills/)
- [API Reference](docs/api/)

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 0.9.0 | 2026-04-19 | Production ready |
| 0.8.0 | 2026-04-11 | Platform engineering |
| 0.7.0 | 2026-04-11 | AI engine integration |
| 0.6.0 | 2026-04-11 | L1 infrastructure |
| 0.5.0 | 2026-04-11 | QA & security |

## License

MIT License - see [LICENSE](LICENSE) for details.

---

Built with ❤️ by Project Helix
