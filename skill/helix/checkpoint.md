# /helix-checkpoint - 检查点技能

> 状态持久化与跨会话连续性

## 概述

`/helix-checkpoint` 保存和恢复工作状态，支持跨会话连续性。

## 命令

```bash
# 保存检查点
helix checkpoint save "完成用户 API"

# 列出检查点
helix checkpoint list

# 恢复检查点
helix checkpoint restore 20260419-143000

# 查看状态
helix checkpoint status
```

## 功能

- 保存工作状态
- 记录剩余任务
- 追踪决策
- Git 状态集成

## 数据存储

检查点保存在 `.helix/checkpoints/` 目录

## 示例

```bash
# 保存当前状态
helix checkpoint save "开发用户管理功能" --remaining "添加测试,完善文档"

# 恢复之前状态
helix checkpoint restore 20260419-143000

# 查看所有检查点
helix checkpoint list
```

## 输出

```json
{
  "id": "20260419-143000",
  "label": "完成用户 API",
  "branch": "feature/user-api",
  "remaining_work": ["添加测试", "完善文档"],
  "decisions": ["使用 FastAPI", "SQLite 存储"]
}
```

## 配置

```yaml
checkpoint:
  auto_save: true
  directory: .helix/checkpoints
  include_git: true
```

## 关联技能

- `/helix-learn` - 知识持久化
