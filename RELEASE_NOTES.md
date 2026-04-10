# Project Helix v0.1.0 - Initial Release

> AI Era Software Engineering Methodology - A New Paradigm

---

## 🎉 Welcome to Project Helix

We're thrilled to announce the first release of **Project Helix**, an AI agent-agnostic software engineering framework.

---

## 🚀 What's New

### Core Features

| Feature | Description | Status |
|---------|-------------|--------|
| `/spec` | Transform requirements into structured specifications | ✅ |
| `/build` | Generate code skeleton from specifications | ✅ |
| `/verify` | Automated verification (static, test, acceptance) | ✅ |
| LLM Integration | Enhanced code generation with AI | ✅ |

### Technical Achievements

- **i18n Complete**: Full English internationalization
- **CLI Ready**: Command-line interface with rich output
- **Multi-engine Support**: Architecture ready for Claude Code, OpenClaw, Cursor, and more

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

# 2. Generate Code Skeleton
helix build SPEC.md -o ./my-project

# 3. Verify Code
cd my-project
helix verify
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
│   │   └── verify.py   # Automated verification
│   └── adapters/       # AI engine adapters
├── docs/               # Documentation
└── tests/              # Tests
```

---

## 🤝 Join Us

- **Website**: (Coming Soon)
- **GitHub**: https://github.com/opensourceclaw/helix
- **License**: Apache 2.0

---

## 📝 Changelog

- All source code internationalized to English
- Project Helix branding applied
- Author updated to Peter Cheng
- CLI status command enhanced

---

## 🔜 What's Next

- More skill integrations
- Enhanced LLM capabilities
- Plugin system
- Documentation expansion

---

**Built with ❤️ by Peter Cheng**

*In the AI era, human creativity is the only differentiator.*
