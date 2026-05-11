# GStack Fusion - Best Practices

Usage recommendations from real project experience.

---

## Code Quality Best Practices

### 1. Always Run Code Review

```bash
# Before every commit
/review
```

**Why**:
- Catch potential issues
- Ensure code standards
- Get AI independent opinion

**When**:
- Before merging
- After completing important features
- At code review gate

### 2. Use Fix-First Principle

GStack Fusion skills auto-fix auto-fixable issues.

```bash
# Run review, skills will auto-fix:
# - Formatting issues
# - Missing imports
# - Obvious bugs

/review
```

**Principles**:
- Accept auto-fixes
- Focus on issues requiring human judgment

---

## Testing Best Practices

### 1. Use Correct Testing Tier

```bash
# Quick validation
/qa --tier=quick

# Full test
/qa
```

| Scenario | Recommended Tier |
|----------|------------------|
| Bug fix validation | quick |
| Feature merge | standard |
| Before release | full |

### 2. Test Coverage Requirements

Follow **Beyonce Rule**:

```
Code without tests = code that doesn't exist
```

**Minimum requirements**:
- Core logic > 80% coverage
- Every bug fix must have regression test
- New features must have test cases

---

## Release Best Practices

### 1. Use Complete Release Workflow

```bash
# One-click release with all gates
/ship
```

**Gate checks**:
- ✅ Tests pass
- ✅ Linting passes
- ✅ Type checking passes
- ✅ Codex review passes
- ✅ Changelog updated

### 2. Write Clear Commit Messages

```bash
# Use conventional commits
feat: add user login feature
fix: resolve database connection leak
docs: update API documentation
test: add user authentication tests
refactor: simplify payment processing
```

---

## Debugging Best Practices

### 1. Use Systematic Investigation

```bash
# Don't guess, use investigation framework
/investigate
```

**Investigation flow**:
1. Collect evidence
2. Analyze root cause
3. Form hypothesis
4. Implement fix
5. Verify

### 2. No Fix Without Root Cause

```bash
# ❌ Bad - treat symptoms
# "Added try-catch, problem disappeared"

# ✅ Good - fix root cause
# "Found connection pool exhausted, added connection reuse"
```

---

## Security Best Practices

### 1. Regular Security Audits

```bash
# Daily scan (low noise)
/cso --mode=daily

# Deep scan (monthly)
/cso --mode=comprehensive
```

### 2. Security Gates

```bash
# Security check auto-included in /ship workflow
# No need to run separately
```

---

## Learning Best Practices

### 1. Record Every Error

```bash
# Add learning after every issue
/learn add "bug-type" "what-happened-and-why"

# Example
/learn add "auth-token-expired" "Token not refreshed after 1 hour"
```

### 2. Use Prior Knowledge

```bash
# Search previous errors
/learn search "database"

# Skills will auto-prompt during debugging
```

---

## Design Best Practices

### 1. Consult Before Designing

```bash
# Before starting code
/design-consultation

# Get:
# - Design system recommendations
# - Component structure
# - Interaction patterns
```

### 2. Use Design Review

```bash
# Verify after implementation
/design-review

# Check:
# - Consistency
# - Accessibility
# - Responsiveness
# - Performance
```

---

## Collaboration Best Practices

### 1. Use Checkpoint to Save Progress

```bash
# Save current work state
/checkpoint save "feature-in-progress"

# Can restore on any branch
/checkpoint restore "feature-in-progress"
```

### 2. Clear Communication

```bash
# Use skill status reporting
# DONE - completed successfully
# BLOCKED - blocked
# NEEDS_CONTEXT - need more info
```

---

## Anti-Patterns (Don't Do This)

| Anti-Pattern | Correct Approach |
|--------------|------------------|
| "Commit first, fix later" | Use Feature Flags |
| "This is simple, no tests needed" | Follow Beyonce Rule |
| "It'll be fine" | Assume and verify |
| "Users won't do that" | Test edge cases |
| "I'll add tests later" | Tests are part of code |

---

## Performance Best Practices

### 1. Use Performance Benchmark

```bash
# Establish baseline
/benchmark --baseline

# Check regression on every PR
/benchmark --compare
```

### 2. Monitor Production

```bash
# Post-release monitoring
/canary

# Check:
# - Console errors
# - Performance regression
# - Page failures
```

---

## Summary

| Principle | Action |
|-----------|--------|
| Completeness | Use complete workflows |
| Automation | Accept auto-fixes |
| Verification | Every claim needs evidence |
| Recording | Use learning system |
| Security | Regular audits |

---

*Follow these best practices to maximize GStack Fusion's value.*
