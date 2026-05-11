# /helix-verify - 验证技能

> 自动化代码验证

## 概述

`/helix-verify` 运行静态检查、测试和验收标准验证。

## 命令

```bash
helix verify
helix verify --level static  # 仅静态检查
helix verify --level test    # 运行测试
helix verify --level full    # 完整验证
```

## 验证级别

| 级别 | 检查项 |
|------|--------|
| static | ruff, mypy, 结构检查 |
| test | pytest 运行 |
| acceptance | 验收标准检查 |
| full | 全部检查 |

## 输出

生成验证报告：

```json
{
  "success": true,
  "static": {"passed": true, "issues": []},
  "test": {"passed": true, "tests": 45, "failures": 0},
  "acceptance": {"passed": true, "criteria_met": 5}
}
```

## 配置

```yaml
verify:
  level: full
  timeout: 300
  coverage_threshold: 80
```

## 关联技能

- `/helix-spec` - 验证是否符合规格
- `/helix-build` - 验证生成代码
