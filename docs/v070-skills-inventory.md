# GStack Fusion v0.7.0 Skills Inventory

**Date**: 2026-05-11

---

## Summary

- **Total skills**: 27
- **Categories**: 8 (SDLC-based)
- **Sources**: GStack (16), agent-skills (5), mattpocock (5), Agent-Skills personas (3)
- **New in v0.7.0**: 10 skills from agent-skills and mattpocock/skills

---

## Skills by Category

### planning/ (6 skills)

| Skill | Source | Description |
|-------|--------|-------------|
| office-hours | GStack | YC product discovery |
| plan-ceo-review | GStack | Strategic challenge review |
| autoplan | GStack | End-to-end planning pipeline |
| spec-driven | agent-skills | Spec-first development |
| write-prd | mattpocock | PRD writing |
| prd-to-issues | mattpocock | PRD → Issues |

### architecture/ (3 skills)

| Skill | Source | Description |
|-------|--------|-------------|
| plan-eng-review | GStack | Architecture review |
| design-review | GStack | UI/UX audit |
| improve-architecture | mattpocock | Architecture improvement |

### implementation/ (3 skills)

| Skill | Source | Description |
|-------|--------|-------------|
| codex | GStack | AI coding agent |
| review | GStack | Code review |
| code-reviewer | Agent-Skills | Senior engineer persona |

### quality/ (4 skills)

| Skill | Source | Description |
|-------|--------|-------------|
| qa | GStack | Browser testing |
| qa-engineer | Agent-Skills | QA engineer persona |
| tdd | mattpocock | TDD cycle |
| code-simplify | agent-skills | Code simplification |

### debugging/ (2 skills)

| Skill | Source | Description |
|-------|--------|-------------|
| investigate | GStack | Root cause analysis |
| diagnose | mattpocock | Systematic debugging |

### process/ (4 skills)

| Skill | Source | Description |
|-------|--------|-------------|
| retro | GStack | Engineering retrospective |
| git-workflow | agent-skills | Trunk-based development |
| ci-cd | agent-skills | CI/CD pipeline |
| context-engineering | agent-skills | Context management |

### deploy/ (3 skills)

| Skill | Source | Description |
|-------|--------|-------------|
| ship | GStack | Ship with gates |
| canary | GStack | Canary deployment |
| land-and-deploy | GStack | Production deploy |

### security/ (2 skills)

| Skill | Source | Description |
|-------|--------|-------------|
| cso | GStack | Security audit (OWASP+STRIDE) |
| security-auditor | Agent-Skills | Security engineer persona |

---

## Sources

| Source | Repo | Skills Contributed |
|--------|------|--------------------|
| GStack | garrytan/gstack | 16 |
| agent-skills | addyosmani/agent-skills | 5 |
| mattpocock/skills | mattpocock/skills | 5 |
| Agent-Skills | (personas) | 3 |
| GStack Fusion | (native) | 1 (gstack-interceptor) |

---

## Merge Conflicts Handled

| Skill | GStack | External | Decision |
|-------|--------|----------|----------|
| review | ✅ Kept | agent-skills code-review | GStack version retained |
| ship | ✅ Kept | agent-skills ship | GStack version retained |
| qa | ✅ Kept | mattpocock qa (deprecated) | GStack version retained |
