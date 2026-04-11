# Project Helix

> AI Era Software Engineering Methodology - A New Paradigm
>
> **Version: 1.0.0** | Status: ✅ Stable (Production Ready)

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10+-green.svg)](https://www.python.org)
[![Status](https://img.shields.io/badge/Status-Stable-green.svg)](#)
[![Test Coverage](https://img.shields.io/badge/Coverage-23%25-yellow.svg)](#)

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

## 12 Skills

Helix provides 12 skills organized in 4 layers:

### L1: Execution Engine

| Skill | Description | Status |
|-------|-------------|--------|
| `/spec` | Convert requirement to specification | Beta 🧪 |
| `/build` | Generate code skeleton from spec | Beta 🧪 |
| `/verify` | Run static checks and tests | Beta 🧪 |
| `/ship` | Release and delivery | Beta 🧪 |

### L2: Quality Assurance

| Skill | Description | Status |
|-------|-------------|--------|
| `/review` | Code review | Beta 🧪 |
| `/test` | Intelligent test generation | Beta 🧪 |
| `/audit` | Security audit | Beta 🧪 |
| `/gate` | Quality gate | Beta 🧪 |

### L3: Infrastructure

| Skill | Description | Status |
|-------|-------------|--------|
| `/browse` | Browser control for QA | Beta 🧪 |
| `/design` | Design generation | Beta 🧪 |
| `/learn` | Continuous learning | Beta 🧪 |
| `/checkpoint` | State persistence | Beta 🧪 |

## CLI Commands

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
