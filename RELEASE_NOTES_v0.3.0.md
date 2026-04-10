# Project Helix v0.3.0 - Complete Development Workflow

> AI Era Software Engineering Methodology - A New Paradigm

---

## 🎉 What's New in v0.3.0

### Core Skills (Complete Development Workflow)

| Skill | Description | Status |
|-------|-------------|--------|
| `/spec` | Transform requirements into specifications | ✅ |
| `/build` | Generate code from specifications | ✅ |
| `/verify` | Automated verification | ✅ |
| **`/review`** | Code review and analysis | 🆕 |
| **`/ship`** | Release and delivery | 🆕 |
| **`/qa`** | Testing automation | 🆕 |

### /review Skill Features

- SQL safety checking
- Shell injection detection
- Race condition analysis
- Hardcoded secrets detection
- Error handling review
- Confidence scoring (1-10)

### /ship Skill Features

- Create pull request
- Auto-merge PR
- Version bumping (major/minor/patch)
- Deploy pipeline support
- Dry run mode

### /qa Skill Features

- Run unit/integration/e2e tests
- Coverage analysis
- Test report generation
- Slow test detection
- Failed test tracking

---

## 📦 Installation

```bash
pip install helix-ai
```

Or development mode:

```bash
cd helix
pip install -e .
```

---

## 💻 Quick Start

```bash
# 1. Generate Specification
helix spec "I want to build a user login feature"

# 2. Generate Code
helix build SPEC.md -o ./my-project

# 3. Run Tests
cd my-project
helix qa

# 4. Code Review
helix review

# 5. Ship
helix ship --mode merge
```

---

## 🏗️ Architecture

```
helix/
├── src/helix/
│   ├── core/           # Core orchestration
│   ├── skills/         # Skill implementations
│   │   ├── spec.py     # Specification generation
│   │   ├── build.py    # Code skeleton generation
│   │   ├── verify.py   # Automated verification
│   │   ├── review.py   # Code review (NEW)
│   │   ├── ship.py     # Release & delivery (NEW)
│   │   └── qa.py       # Testing automation (NEW)
│   └── adapters/       # AI engine adapters
├── docs/               # Documentation
└── tests/              # Tests
```

---

## 📝 Changelog (since v0.2.0)

- Added /review skill for code analysis
- Added /ship skill for release workflow
- Added /qa skill for testing automation
- CLI commands: helix review, helix ship, helix qa

---

## 🔜 What's Next (v0.4.0)

- Plugin system architecture
- Claude Code integration
- OpenClaw integration
- Enhanced LLM capabilities
- CI/CD pipeline integration

---

## 🤝 Project Helix

**Project Helix** is a human-AI co-creation project, built through the collaboration of:

- **Peter Cheng** - Human architect and decision maker
- **Jarvis** - AI coding assistant

This represents a new paradigm of software engineering in the AI era.

---

**Built with ❤️ by Peter Cheng + Jarvis**

*In the AI era, human creativity is the only differentiator.*
