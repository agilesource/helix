# /helix-learn - 持续学习技能

> 项目知识持续学习与记忆

## 概述

`/helix-learn` 记录和管理项目学习成果，支持跨会话知识复用。

## 命令

```bash
# 添加学习
helix learn add --key "python-async" --insight "使用 asyncio.gather 并发执行"

# 查看学习
helix learn

# 搜索
helix learn search "python"

# 统计
helix learn stats

# 导出
helix learn export
```

## 学习类型

| 类型 | 描述 |
|------|------|
| pattern | 代码模式 |
| pitfall | 陷阱/坑 |
| best-practice | 最佳实践 |
| bug | Bug 记录 |

## 数据存储

学习记录保存在 `.helix/learnings.jsonl`

## 示例

```bash
# 添加学习
helix learn add --key "fastapi-router" --insight "使用 APIRouter 模块化路由"

# 搜索
helix learn search "api"

# 导出为 Markdown
helix learn export --format markdown
```

## 配置

```yaml
learn:
  storage: .helix/learnings.jsonl
  auto_dedupe: true
  confidence_threshold: 7
```

## 关联技能

所有技能都可以利用学习系统进行知识积累
