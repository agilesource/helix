# /helix-audit - 安全审计技能

> 自动化安全漏洞扫描

## 概述

`/helix-audit` 扫描代码中的安全漏洞和风险。

## 命令

```bash
helix audit
helix audit --level basic   # 基础检查
helix audit --level deep    # 深度扫描
```

## 检查项

- 依赖漏洞
- 代码安全问题
- 配置风险
- 秘钥泄露
- SQL 注入
- XSS 漏洞

## 输出

```json
{
  "findings": [
    {"severity": "high", "type": "sql_injection", "file": "db.py"},
    {"severity": "medium", "type": "hardcoded_key", "file": "config.py"}
  ]
}
```

## 配置

```yaml
audit:
  level: deep
  check_dependencies: true
```

## 关联技能

- `/helix-review` - 代码审查
