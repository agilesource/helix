# Helix AI Engineering

> AI Era Software Engineering Methodology - A New Paradigm
>
> **Version: 1.1.0** | Status: ✅ Production Ready

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10+-green.svg)](https://www.python.org)
[![Status](https://img.shields.io/badge/Status-Production-green.svg)](#)
[![Skills](https://img.shields.io/badge/Skills-33-orange.svg)](#)

## Core Philosophy

> When the marginal cost of code generation approaches zero, architectural clarity, requirement precision, and test completeness become the sole differentiators for human-created value.

Helix is an AI agent-agnostic software engineering framework that supports multiple AI engines as execution backends. Now powered by the world's best AI engineering skills from Garry Tan, Addy Osmani, Matt Pocock, and more.

## Three Pillars Integration

| Pillar | Core Value | Helix Mapping |
|--------|------------|---------------|
| **Skills** | 33 production-grade skills | 8 SDLC categories |
| **Methodology** | Google Engineering Practices | Rationalization + Verification |
| **Tools** | CLI + Design System | helix-ai + DESIGN.md |

## Installation

### CLI Tool

```bash
pip install helix-ai
```

Or development mode:

```bash
cd helix
pip install -e .
```

### Skills Framework

The skills can be used with Claude Code, OpenClaw, or any AI coding agent:

```bash
# Copy skills to your AI agent's skills directory
cp -r skills ~/.claude/skills/helix
```

## Quick Start

### Using CLI

```bash
helix spec "I want to build a user login feature"
helix build SPEC.md -o ./my-project
cd my-project && helix verify
```

### Using Skills

In your AI coding agent, invoke skills by name:

```bash
/office-hours    # YC product discovery
/plan-ceo-review # Strategic challenge
/spec-driven     # Spec before code
/tdd             # Test-driven development
/review          # Code review
/qa              # Browser testing
/ship            # Ship with gates
/cso             # Security audit
```

## 33 Skills in 8 Categories

### planning (6)

| Skill | Description | Source |
|-------|-------------|--------|
| `/office-hours` | YC product discovery with 6 forcing questions | GStack |
| `/plan-ceo-review` | Strategic challenge with 4 scope modes | GStack |
| `/spec-driven` | Write spec before code | agent-skills |
| `/write-prd` | Product requirements document | mattpocock |
| `/prd-to-issues` | Convert PRD to GitHub Issues | mattpocock |
| `/helix-spec` | Helix specification generation | Helix |

### architecture (3)

| Skill | Description | Source |
|-------|-------------|--------|
| `/plan-eng-review` | Architecture review | GStack |
| `/design-review` | UI/UX audit, catch AI slop | GStack |
| `/improve-architecture` | Codebase architecture improvement | mattpocock |

### implementation (3)

| Skill | Description | Source |
|-------|-------------|--------|
| `/codex` | AI coding agent with full project awareness | GStack |
| `/review` | Staff engineer code review | GStack |
| `/code-reviewer` | Senior Engineer persona | Agent-Skills |

### quality (5)

| Skill | Description | Source |
|-------|-------------|--------|
| `/qa` | Real browser testing with headless Chromium | GStack |
| `/qa-engineer` | QA Engineer persona | Agent-Skills |
| `/tdd` | Test-driven development (red-green-refactor) | mattpocock |
| `/code-simplify` | Code simplification | agent-skills |
| `/helix-gate` | Quality gate | Helix |

### debugging (2)

| Skill | Description | Source |
|-------|-------------|--------|
| `/investigate` | Root cause debugging | GStack |
| `/diagnose` | System debugging methodology | mattpocock |

### process (9)

| Skill | Description | Source |
|-------|-------------|--------|
| `/retro` | Weekly engineering retrospective | GStack |
| `/git-workflow` | Trunk-based development | agent-skills |
| `/ci-cd` | CI/CD pipeline automation | agent-skills |
| `/context-engineering` | Context management | agent-skills |
| `/autoplan` | End-to-end feature planning | GStack |
| `/learn` | Continuous learning | GStack |
| `/checkpoint` | State persistence | GStack |
| `/helix-build` | Helix code generation | Helix |
| `/helix-verify` | Helix verification | Helix |

### deploy (3)

| Skill | Description | Source |
|-------|-------------|--------|
| `/ship` | Ship with gates | GStack |
| `/canary` | Canary deployment | GStack |
| `/land-and-deploy` | Production deployment | GStack |

### security (2)

| Skill | Description | Source |
|-------|-------------|--------|
| `/cso` | Security audit (OWASP + STRIDE) | GStack |
| `/security-auditor` | Security Engineer persona | Agent-Skills |

## Project Structure

```
helix/
├── VERSION                     # v1.1.0
├── skills/                     # 33 skills in 8 categories
│   ├── planning/              (6)
│   ├── architecture/          (3)
│   ├── implementation/        (3)
│   ├── quality/               (5)
│   ├── debugging/             (2)
│   ├── process/               (9)
│   ├── deploy/                (3)
│   └── security/              (2)
├── skill.bak/                 # Original 12 Helix skills (backup)
├── bin/                       # GStack tool scripts
├── lib/                       # Shared libraries
├── docs/                      # Documentation
│   ├── methodology/           # Engineering methodology
│   ├── SKILLS_REFERENCE.md    # Skills reference
│   └── QUICKSTART.md          # Quick start guide
├── DESIGN.md                  # Brand design system
├── src/helix/                 # Helix Python core
├── tests/                     # Test suite
├── README.md
└── CHANGELOG.md
```

## Credits

Helix integrates skills from the world's leading AI engineering practitioners:

- **Garry Tan** (YC CEO) - office-hours, plan-ceo-review, codex
- **Addy Osmani** (Google) - spec-driven, TDD, CI/CD
- **Matt Pocock** - write-prd, diagnose, improve-architecture
- **Agent-Skills Team** - quality gates, code review process

## Vision, Mission, Values

See [docs/brainstorming/VMV.md](docs/brainstorming/2026-04-09_Helix_VMV.md)

## License

Apache License 2.0 - see [LICENSE](LICENSE) file for details.

---

*Helix AI Engineering - The World's First Integrated AI Software Engineering Framework*
