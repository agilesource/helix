# /helix-ship - 发布技能

> 代码发布与交付

## 概述

`/helix-ship` 自动化版本管理、PR 创建和发布流程。

## 命令

```bash
helix ship
helix ship --mode create-pr  # 创建 PR
helix ship --mode merge      # 创建并合并
helix ship --mode deploy     # 部署
```

## 发布模式

| 模式 | 描述 |
|------|------|
| create-pr | 创建 Pull Request |
| merge | 创建并合并 PR |
| deploy | 部署到生产环境 |

## 工作流

1. 版本号更新
2. CHANGELOG 更新
3. Git commit
4. 创建 PR / Tag
5. 部署 (可选)

## 配置

```yaml
ship:
  mode: create-pr
  auto_merge: false
  bump_version: true
  version_type: patch  # major, minor, patch
```

## 示例

```bash
# 创建 PR
helix ship --mode create-pr

# 自动合并
helix ship --mode merge

# 部署
helix ship --mode deploy
```

## 关联技能

- `/helix-verify` - 发布前验证
