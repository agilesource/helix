"""
Helix Documentation Generator

Auto-generate project documentation:
- README.md
- ARCHITECTURE.md
- API documentation
- CHANGELOG
"""

import json
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime


def generate_readme(project_name: str = "Helix", description: str = "") -> str:
    """Generate README.md"""

    if not description:
        description = "AI Era Software Engineering Methodology - Human-AI Co-evolution Framework"

    return f"""# {project_name}

> {description}

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
| 0.9.0 | {datetime.now().strftime('%Y-%m-%d')} | Production ready |
| 0.8.0 | 2026-04-11 | Platform engineering |
| 0.7.0 | 2026-04-11 | AI engine integration |
| 0.6.0 | 2026-04-11 | L1 infrastructure |
| 0.5.0 | 2026-04-11 | QA & security |

## License

MIT License - see [LICENSE](LICENSE) for details.

---

Built with ❤️ by Project Helix
"""


def generate_architecture_doc() -> str:
    """Generate ARCHITECTURE.md"""

    return f"""# Helix Architecture

> Last Updated: {datetime.now().strftime('%Y-%m-%d')}

## Design Principles

1. **Human at the Helm** - AI is the executor, not the decision maker
2. **Quality Obsessed** - Quality is the only competitive advantage
3. **Evolve Gradually** - Continuous iteration, no perfectionism
4. **Open Collaboration** - Collective wisdom
5. **Tools Serve Humans** - Technology serves people

## Four-Layer Architecture

```
┌─────────────────────────────────────────────────────────────┐
│  L4: Meta-Methodology                                       │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐          │
│  │  Agile  │ │ DevOps  │ │Platform │ │Harness  │          │
│  └─────────┘ └─────────┘ └─────────┘ └─────────┘          │
├─────────────────────────────────────────────────────────────┤
│  L3: Execution Engine                                       │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐          │
│  │  /spec  │ │ /build  │ │/verify  │ │ /ship   │          │
│  └─────────┘ └─────────┘ └─────────┘ └─────────┘          │
├─────────────────────────────────────────────────────────────┤
│  L2: Quality Assurance                                      │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐          │
│  │/review  │ │ /test   │ │ /audit  │ │  /gate  │          │
│  └─────────┘ └─────────┘ └─────────┘ └─────────┘          │
├─────────────────────────────────────────────────────────────┤
│  L1: Infrastructure                                         │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐          │
│  │/browse  │ │ /design │ │ /learn  │ │/checkpoint│         │
│  └─────────┘ └─────────┘ └─────────┘ └─────────┘          │
└─────────────────────────────────────────────────────────────┘
```

## Core Components

### Intent Recognition

Natural language processing to route user requests to appropriate skills.

```
User Input → Intent Recognizer → Skill Router → Execution
```

### AI Engine Manager

Multi-engine orchestration with:
- Automatic failover
- Load balancing
- Health monitoring

### Plugin System

Extensible architecture supporting:
- Skill plugins
- Adapter plugins
- Integration plugins

## Data Flow

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│   User CLI   │────▶│   API Server │────▶│  Orchestrator│
└──────────────┘     └──────────────┘     └──────────────┘
                                                  │
                    ┌─────────────────────────────┼─────────────┐
                    │                             │             │
              ┌─────▼─────┐              ┌──────▼──────┐ ┌────▼────┐
              │  Skills   │              │ AI Engines  │ │Monitoring│
              └───────────┘              └─────────────┘ └─────────┘
```

## Technology Stack

- **Language**: Python 3.10+
- **CLI**: Click
- **API**: FastAPI
- **Async**: asyncio
- **Type Checking**: mypy

## Security

- Input validation on all endpoints
- Secret encryption in plugin config
- Sandboxed skill execution
- Audit logging

## Performance

- Async execution throughout
- Request queuing
- Connection pooling
- Caching layer (planned)

---

*Generated by Helix Documentation System*
"""


def generate_changelog(existing_changelog: str = "") -> str:
    """Generate or update CHANGELOG"""

    new_entries = f"""# Changelog

## v0.9.0 - {datetime.now().strftime('%Y-%m-%d')} - Production Ready

### Added
- Performance monitoring system
- Health check endpoints
- Complete documentation
- Production configuration templates

### Improved
- Error handling
- Performance optimization

### Fixed
- Various bug fixes

## v0.8.0 - 2026-04-11 - Platform Engineering

### Added
- REST API server
- CI/CD integration
- Webhook handlers

## v0.7.0 - 2026-04-11 - AI Engine Integration

### Added
- AI Engine Manager
- Intent Recognition
- Claude Code adapter
- OpenClaw adapter

## v0.6.0 - 2026-04-11 - L1 Infrastructure

### Added
- Browse skill
- Design skill
- Learn skill
- Checkpoint skill

## v0.5.0 - 2026-04-11 - QA & Security

### Added
- Audit skill
- Gate skill

---

*Auto-generated by Helix*
"""

    return new_entries


def run_docs_generator(output_dir: str = ".") -> None:
    """Run documentation generator"""

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # Generate README
    readme = generate_readme()
    (output_path / "README.md").write_text(readme)
    print(f"Generated: {output_path}/README.md")

    # Generate Architecture
    arch = generate_architecture_doc()
    (output_path / "ARCHITECTURE.md").write_text(arch)
    print(f"Generated: {output_path}/ARCHITECTURE.md")

    # Generate Changelog
    changelog = generate_changelog()
    (output_path / "CHANGELOG.md").write_text(changelog)
    print(f"Generated: {output_path}/CHANGELOG.md")


if __name__ == "__main__":
    import sys
    output = sys.argv[1] if len(sys.argv) > 1 else "."
    run_docs_generator(output)
