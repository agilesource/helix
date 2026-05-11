# Helix Quick Start Guide

## 5 Minute Quick Start

### Prerequisites

- Python 3.10+
- Git
- (Optional) Claude Code, OpenClaw, or any AI coding agent

---

## Option 1: Using CLI

### 1. Install Helix

```bash
pip install helix-ai
```

Or development mode:

```bash
cd helix
pip install -e .
```

### 2. Generate Specification

```bash
helix spec "I want to build a user login feature"
```

This creates a `SPEC.md` file with detailed requirements.

### 3. Generate Code

```bash
helix build SPEC.md -o ./my-project
```

### 4. Verify

```bash
cd my-project
helix verify
```

---

## Option 2: Using Skills (Recommended)

### 1. Set Up Skills

Copy skills to your AI agent:

```bash
# For Claude Code
mkdir -p ~/.claude/skills
cp -r helix/skills ~/.claude/skills/helix

# For OpenClaw
cp -r helix/skills ~/.openclaw/skills/
```

### 2. Use Skills in AI Agent

Start a conversation with your AI coding agent:

```
/office-hours
"I want to build a daily briefing app"
```

The AI will guide you through 6 forcing questions to clarify your product idea.

### 3. Plan Your Work

```
/plan-ceo-review
"Our team wants to add notifications"
```

Get strategic challenge with 4 scope modes.

### 4. Write Spec First

```
/spec-driven
Build a user authentication system with email/password and OAuth
```

Always write spec before code.

### 5. Implement with TDD

```
/tdd
Implement user authentication
```

Follow red-green-refactor loop.

### 6. Review and Ship

```
/review
# Review your code changes

/qa
# Test in real browser

/ship
# Ship with quality gates
```

---

## Common Workflows

### New Feature

```
/office-hours → /plan-ceo-review → /spec-driven → /tdd → /review → /qa → /ship
```

### Bug Fix

```
/investigate → /tdd → /review → /qa → /ship
```

### Code Improvement

```
/improve-architecture → /code-simplify → /review → /ship
```

---

## Skills by Phase

| Phase | Skills |
|-------|--------|
| **Discovery** | /office-hours, /write-prd |
| **Planning** | /plan-ceo-review, /plan-eng-review, /spec-driven |
| **Implementation** | /codex, /tdd, /autoplan |
| **Review** | /review, /code-reviewer |
| **Testing** | /qa, /qa-engineer |
| **Security** | /cso, /security-auditor |
| **Deploy** | /ship, /canary, /land-and-deploy |
| **Retrospective** | /retro |

---

## Tips

1. **Always start with /office-hours** - Forces clarity on what you're building
2. **Spec before code** - Use /spec-driven for any new feature
3. **Ship with gates** - Never /ship without /review and /qa
4. **Use /retro weekly** - Learn and improve continuously

---

## Next Steps

- Read [SKILLS_REFERENCE.md](./SKILLS_REFERENCE.md) for all 33 skills
- Check [docs/methodology/](./methodology/) for engineering practices
- Explore [DESIGN.md](./DESIGN.md) for brand guidelines
