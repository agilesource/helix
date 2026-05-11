# v0.7.0 Merge Conflicts Record

**Date**: 2026-05-11

---

## Resolved Conflicts

| Skill | Source A | Source B | Decision | Reason |
|-------|----------|----------|----------|--------|
| review | GStack | agent-skills | Keep GStack | GStack version more comprehensive (88KB vs lighter persona) |
| ship | GStack | agent-skills | Keep GStack | GStack has full gate system + deployment workflow |
| qa | GStack | mattpocock (deprecated) | Keep GStack | GStack has real browser (Playwright/Chromium) |

## No Conflicts

The 10 new skills from agent-skills and mattpocock/skills are unique and have no overlap with existing GStack skills.

## Notes

- `code-reviewer` coexists with `review` intentionally: `review/` is the automated PR review workflow, `code-reviewer/` is a persona role for manual review contexts
- `qa-engineer` coexists with `qa` intentionally: `qa/` is automated browser testing, `qa-engineer/` is a persona role
- mattpocock's `qa` was deprecated in source repo, ignored
