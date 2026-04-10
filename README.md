# Project Helix

> AI Era Software Engineering Methodology - A New Paradigm

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10+-green.svg)](https://www.python.org)
[![Status](https://img.shields.io/badge/Status-Alpha-orange.svg)](#)

## Core Philosophy

> When the marginal cost of code generation approaches zero, architectural clarity, requirement precision, and test completeness become the sole differentiators for human-created value.

Helix is an AI agent-agnostic software engineering framework that supports multiple AI engines as execution backends.

## Four Methodologies Integration

| Methodology | Core Value | Helix Mapping |
|-------------|------------|---------------|
| Agile | Rapid iteration | `/spec` Spec-driven |
| DevOps | Full automation | `/verify` Verification loop |
| Platform Engineering | Capability encapsulation | Skills as services |
| Harness Engineering | Human steers, AI executes | Human defines constraints, AI generates code |

## Installation

```bash
pip install helix-ai
```

Or development mode:

```bash
cd helix
pip install -e .
```

## Quick Start

### 1. Generate Specification

```bash
helix spec "I want to build a user login feature"
```

### 2. Generate Code Skeleton

```bash
helix build SPEC.md -o ./my-project
```

### 3. Verify Code

```bash
cd my-project
helix verify
```

## CLI Commands

| Command | Description |
|---------|-------------|
| `helix spec <requirement>` | Convert requirement to specification |
| `helix build <spec-file>` | Generate code skeleton from spec |
| `helix verify [path]` | Run static checks, tests, acceptance |
| `helix templates` | List available templates |
| `helix list-skills` | List all skills |
| `helix status` | View status |

## Supported AI Engines

| Engine | Status |
|--------|--------|
| Claude Code | 🔜 Planned |
| OpenClaw | 🔜 Planned |
| OpenCode | 🔜 Planned |
| Cursor | 🔜 Planned |
| GitHub Copilot CLI | 🔜 Planned |
| Gemini CLI | 🔜 Planned |

## Project Structure

```
helix/
├── src/helix/
│   ├── core/           # Core orchestration
│   ├── skills/         # Skill implementations
│   │   ├── spec.py     # Specification generation
│   │   ├── build.py    # Code skeleton generation
│   │   └── verify.py   # Automated verification
│   └── adapters/       # AI engine adapters
├── docs/               # Documentation
└── tests/              # Tests
```

## Vision, Mission, Values

See [docs/brainstorming/VMV.md](docs/brainstorming/2026-04-09_Helix_VMV.md)

## License

Apache License 2.0 - see [LICENSE](LICENSE) file for details.
