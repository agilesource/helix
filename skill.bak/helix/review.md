# /helix-review - 代码审查技能

> AI 驱动的代码审查

## 概述

`/helix-review` 使用 LLM 进行代码审查，提供改进建议。

## 命令

```bash
helix review
helix review ./src
helix review --diff-only  # 仅审查变更
```

## 检查项

- 代码质量
- 安全漏洞
- 性能问题
- 最佳实践
- 文档完整性

## 输出

```markdown
## 审查报告

### 问题 (3)
- [高] 安全风险: SQL 注入
- [中] 性能: N+1 查询
- [低] 风格: 命名不一致

### 建议
- 使用参数化查询
- 添加数据库索引
```

## 配置

```yaml
review:
  focus: security  # security, performance, style
  auto_fix: false
```

## 关联技能

- `/helix-verify` - 验证修复
