# Project Helix v0.4.0 - Plugin System & AI Engine Integration

> AI Era Software Engineering Methodology - A New Paradigm

---

## 🎉 What's New in v0.4.0

### Core Feature: Plugin System

| Component | Description | Status |
|-----------|-------------|--------|
| Plugin Base Classes | Plugin, SkillPlugin, AdapterPlugin | ✅ |
| Plugin Manager | Discovery, loading, lifecycle | ✅ |
| Plugin Config | Settings and permissions | ✅ |
| CLI Command | `helix plugins` | ✅ |

### AI Engine Adapters

| Adapter | Description | Status |
|---------|-------------|--------|
| Claude Code | Claude Code CLI integration | ✅ |
| Anthropic API | Direct API access | ✅ |
| OpenClaw | OpenClaw framework integration | ✅ |

### Example Plugin

- **hello_world** - Demo skill plugin in `plugins/` directory

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
# List plugins
helix plugins

# Use skills
helix spec "user login"
helix build SPEC.md
helix review
helix qa
helix ship --mode merge
```

---

## 🔧 Plugin Development

```python
from helix.plugins.base import Plugin, PluginMetadata, SkillPlugin

class MySkillPlugin(SkillPlugin):
    metadata = PluginMetadata(
        name="my-plugin",
        version="0.1.0",
        description="My custom plugin",
    )

    def get_skill_class(self):
        return MySkillClass
```

Save to `plugins/my_plugin.py` and it will be auto-discovered!

---

## 🏗️ Architecture

```
helix/
├── src/helix/
│   ├── core/           # Core orchestration
│   ├── skills/         # Built-in skills (spec, build, verify, review, ship, qa)
│   ├── plugins/        # Plugin system (NEW)
│   │   ├── base.py     # Plugin base classes
│   │   ├── manager.py  # Plugin manager
│   │   └── config.py   # Configuration
│   └── adapters/       # AI engine adapters
│       ├── claude_code_adapter.py   (NEW)
│       └── openclaw_adapter.py      (NEW)
├── plugins/            # Custom plugins
│   └── hello_world.py  # Example plugin
└── docs/
    └── roadmap/        # v0.4.0 roadmap
```

---

## 📝 Changelog (since v0.3.0)

- Added complete plugin system
- Added Plugin base classes (Plugin, SkillPlugin, AdapterPlugin)
- Added PluginManager with discovery and lifecycle
- Added plugin configuration management
- Added Claude Code adapter
- Added Anthropic API adapter
- Added OpenClaw adapter
- Added example hello_world plugin
- Added `helix plugins` CLI command
- Updated roadmap documentation

---

## 🔜 What's Next (v1.0.0)

- Plugin marketplace
- Enhanced AI capabilities
- More built-in skills
- Documentation expansion
- Production-ready stability

---

## 🤝 Project Helix

**Project Helix** is a human-AI co-creation project, built through the collaboration of:

- **Peter Cheng** - Human architect and decision maker
- **Jarvis** - AI coding assistant

This represents a new paradigm of software engineering in the AI era.

---

**Built with ❤️ by Peter Cheng + Jarvis**

*In the AI era, human creativity is the only differentiator.*
