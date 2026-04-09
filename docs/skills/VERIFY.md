# Helix /verify Skill Design

> **Version**: v0.1
> **Status**: Detailed Design

---

## 1. Skill Overview

| Attribute | Value |
|-----------|-------|
| Name | `/verify` |
| Category | Execution (Execution Engine) |
| Dependencies | `/spec`, `/build` |
| Core Function | Automated verification loop |

---

## 2. Workflow

```
┌─────────────────────────────────────────────────────────────┐
│                       /verify Workflow                      │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Input: Code directory or test command                      │
│       │                                                     │
│       ▼                                                     │
│  ┌─────────────┐                                           │
│  │ Environment │ ◄── Detect dependencies, language,        │
│  │ Detection   │     framework                              │
│  └─────────────┘                                           │
│       │                                                     │
│       ▼                                                     │
│  ┌─────────────┐                                           │
│  │ Static      │ ◄── lint, type check, format              │
│  │ Checks      │                                           │
│  └─────────────┘                                           │
│       │                                                     │
│       ▼                                                     │
│  ┌─────────────┐                                           │
│  │ Unit Tests  │ ◄── Run test suite                        │
│  └─────────────┘                                           │
│       │                                                     │
│       ▼                                                     │
│  ┌─────────────┐                                           │
│  │ Acceptance  │ ◄── Verify Spec acceptance criteria       │
│  │ Tests       │                                           │
│  └─────────────┘                                           │
│       │                                                     │
│       ▼                                                     │
│  Output: Verification Report                                │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 3. Verification Layers

### 3.1 L1: Static Checks

| Check | Tool | Description |
|-------|------|-------------|
| Code Format | black, ruff | Format standards |
| Type Check | mypy | Type safety |
| Lint | ruff, flake8 | Code quality |
| Security Scan | bandit | Security vulnerabilities |

### 3.2 L2: Unit Tests

| Check | Tool | Description |
|-------|------|-------------|
| Test Run | pytest | Execute tests |
| Coverage | pytest-cov | Coverage check |
| Fast Fail | - | Stop on any test failure |

### 3.3 L3: Acceptance Tests

| Check | Description |
|-------|-------------|
| Spec AC Verification | Verify acceptance criteria line by line |
| Manual Test Points | Mark points requiring manual testing |

---

## 4. CLI Interface

```bash
# Verify current directory
helix verify

# Verify specific directory
helix verify ./src

# Static checks only
helix verify --level static

# Run tests only
helix verify --level test

# Full verification
helix verify --level full

# Acceptance tests
helix verify --level acceptance

# Generate report
helix verify --report json
```

---

## 5. Output Format

### JSON Report

```json
{
  "timestamp": "2026-04-09T12:00:00Z",
  "duration_seconds": 15,
  "levels": {
    "static": {
      "status": "pass",
      "issues": []
    },
    "test": {
      "status": "pass",
      "tests_run": 12,
      "tests_passed": 12,
      "coverage": 85
    },
    "acceptance": {
      "status": "partial",
      "ac_met": 3,
      "ac_total": 5,
      "manual_tests": ["Test payment flow"]
    }
  },
  "overall": "pass"
}
```

### Human-Readable Output

```
╭───────────────────────── Verification Report ──────────────────────────╮
│ Static Checks    ✓ PASS (12s)                                          │
│ Unit Tests       ✓ PASS (85% coverage)                                 │
│ Acceptance Tests ⚠ PARTIAL (3/5 passed)                                │
├──────────────────────────────────────────────────────────────────────────┤
│ Overall Status: ⚠ Manual acceptance required                           │
│                                                                  │
│ Manual Tests Pending:                                                │
│ - [ ] Is payment flow working correctly                            │
│ - [ ] Email verification code sending                              │
╰──────────────────────────────────────────────────────────────────────────╯
```

---

## 6. Open Discussion

1. [ ] Should verification failure block subsequent steps?
2. [ ] How to integrate with CI/CD?
3. [ ] Do we need a "verify Spec AC only" mode?

---

Start implementation or discuss other topics first?
