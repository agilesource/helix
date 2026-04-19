# /helix-gate - 质量门禁技能

> CI/CD 质量门禁

## 概述

`/helix-gate` 在 CI/CD 流程中作为质量门禁，确保代码质量达标。

## 命令

```bash
helix gate
helix gate --threshold 80  # 覆盖率阈值
helix gate --strict        # 严格模式
```

## 检查项

- 测试覆盖率
- 代码质量分数
- 安全检查
- 文档完整性

## 门禁规则

| 规则 | 默认阈值 |
|------|----------|
| 覆盖率 | ≥ 80% |
| mypy | 0 错误 |
| ruff | 0 警告 |
| 安全漏洞 | 0 高危 |

## 输出

```
✓ 测试覆盖率: 85% (≥ 80%)
✓ mypy: 0 错误
✓ ruff: 0 警告
✓ 安全: 无高危漏洞

✅ 质量门禁通过
```

## 配置

```yaml
gate:
  coverage_threshold: 80
  strict: false
  checks: [coverage, mypy, ruff, security]
```

## 关联技能

- `/helix-verify` - 验证
- `/helix-audit` - 安全审计
