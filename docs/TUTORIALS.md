# GStack Fusion - Hands-on Tutorials

Detailed step-by-step demonstrations for real scenarios.

---

## Tutorial 1: Code Review Workflow

### Goal
Review a PR and ensure code quality.

### Steps

```bash
# 1. Run basic review
/review

# Output example:
# Pre-Landing Review: 3 issues (1 critical, 2 informational)
#
# [CRITICAL] (confidence: 9/10) src/auth.py:42 — SQL injection via string
# Fix: Use parameterized query
#
# [INFORMATIONAL] (confidence: 7/10) src/utils.py:15 — Missing type hint
# Fix: Add return type annotation
```

### Key Points

- **Critical issues**: Must fix
- **Informational issues**: Recommended fixes
- **Fix-First**: Skills auto-fix what's auto-fixable

---

## Tutorial 2: Complete QA Testing

### Goal
Test a web application and fix found issues.

### Steps

```bash
# 1. Run QA testing
/qa

# Output example:
# QA Testing: 5 bugs found
#
# 1. [HIGH] Login form - Submit button not working
# 2. [MEDIUM] Dashboard - Slow loading (3s)
# 3. [LOW] Header - Misaligned on mobile
# ...

# 2. Skills auto-fix fixable issues
# [AUTO-FIXED] Login form — Added form handler

# 3. Ask user about complex issues
# Fix Dashboard performance issue?
# A) Yes — B) No
```

### Three Testing Tiers

| Tier | Command | Coverage |
|------|---------|----------|
| Quick | `/qa --tier=quick` | Critical + High |
| Standard | `/qa` | All high priority |
| Full | `/qa --tier=full` | Full test suite |

---

## Tutorial 3: Release Workflow

### Goal
Safely release code to production.

### Steps

```bash
# 1. Run release
/ship

# Output example:
# === Ship Workflow ===
# 1. ✓ Tests passed (47/47)
# 2. ✓ Linting passed
# 3. ✓ Type checking passed
# 4. [GATE] Codex review: PASS
#
# Choose commit message:
# A) feat: add new login feature
# B) fix: resolve login issue
# C) Custom message

# 2. Auto-create PR
# ✓ PR created: https://github.com/.../pull/123

# 3. Wait for merge, then deploy
# ✓ Deployed to production
```

### Gate Checks

| Check | Description |
|-------|-------------|
| Tests | All tests pass |
| Lint | Code style check |
| Type | Type checking |
| Codex Review | AI independent review |
| Changelog | Changelog updated |

---

## Tutorial 4: Debugging Issues

### Goal
Systematically investigate and fix production issues.

### Steps

```bash
# 1. Start investigation
/investigate

# 2. Choose debugging mode
# A) Error investigation (recommended)
# B) Performance issue
# C) Behavior unexpected

# 3. Investigation runs automatically
# Phase 1: Collect evidence
# Phase 2: Analyze root cause
# Phase 3: Form hypothesis
# Phase 4: Implement fix

# Output example:
# ROOT CAUSE FOUND:
# Database connection pool exhausted due to missing cleanup
# in src/db.py:89
#
# Fix applied: Added connection.close() in finally block
```

### Investigation Principles

- **No assumptions**: Every conclusion needs evidence
- **No fix without root cause**: Find root cause before fixing
- **Verify**: Must verify after fixing

---

## Tutorial 5: Design Workflow

### Goal
Create and review UI designs.

### Steps

```bash
# 1. Design consultation
/design-consultation

# Input: "Create a data analytics dashboard"
# Output: Complete design system recommendations

# 2. Generate design variants
/design-shotgun

# Input: "Login page"
# Output: 3 design variants (Modern, Classic, Minimal)

# 3. Review design
/design-review

# Auto-checks:
# - Consistency
# - Spacing
# - Hierarchy
# - Accessibility
```

---

## Tutorial 6: Security Audit

### Goal
Review code for security issues.

### Steps

```bash
# 1. Run security audit
/cso

# Or use Agent Persona
/security-auditor

# Output example:
# SECURITY AUDIT REPORT
# =====================
# Critical: 0
# High: 2
# Medium: 5
# Low: 8
#
# Findings:
# [HIGH] src/auth.py:42 — Hardcoded API key found
# [HIGH] src/payment.py:18 — Missing input validation
# ...
```

### Audit Scope

| Category | Checks |
|----------|--------|
| Secrets | Keys, passwords, tokens |
| Supply Chain | Dependency security |
| Injection | SQL/Command injection |
| Auth | Authentication & authorization |
| OWASP | Top 10 |

---

## Tutorial 7: Learning & Memory

### Goal
Accumulate knowledge across sessions.

```bash
# 1. View learned content
/learn

# Output:
# Learnings: 12 entries
# - pitfall: auth-token-expired (3 occurrences)
# - pattern: postgres-retry-logic
# - preference: use-pydantic-for-validation

# 2. Search related learnings
/learn search "database"

# 3. Add new learning
/learn add "new-pattern" "description"
```

---

## Best Practices

### 1. Always Use Complete Workflows

```bash
# Bad
fix bug → commit → push

# Good
/investigate → fix → /review → /qa → /ship
```

### 2. Use Smart Gates

```bash
# Manual checks
run tests
run lint
check security

# Auto gates
/ship
# All auto-executed
```

### 3. Use Learning System

```bash
# Record every error
/learn add "bug-pattern" "what-went-wrong-and-why"

# Next time similar issue occurs, skills will auto-prompt
```

---

## Next Steps

- [QUICKSTART.md](./QUICKSTART.md) - Quick Start
- [BEST_PRACTICES.md](./BEST_PRACTICES.md) - Best Practices
- [TROUBLESHOOTING.md](./TROUBLESHOOTING.md) - Troubleshooting

---

*Tutorial complete. You can now start using GStack Fusion.*
