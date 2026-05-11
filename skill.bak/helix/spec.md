# /helix-spec - 规格说明技能

> 将用户需求转换为结构化规格说明

## 概述

`/helix-spec` 使用 LLM 将自然语言需求转换为结构化的规格说明文档。

## 命令

```bash
helix spec "创建用户登录功能"
helix spec "实现 REST API"
helix spec --interactive  # 交互模式
```

## 输入

- 自然语言需求描述
- 可选的上下文信息

## 输出

生成 `SPEC.md` 文件，包含：

- 项目概述
- 功能需求
- 接口设计
- 数据模型
- 验收标准

## 示例

### 输入

```
helix spec "创建用户管理 API，需要支持 CRUD 操作"
```

### 输出 (SPEC.md)

```markdown
# 用户管理 API 规格说明

## 项目概述
- 项目名: user-management-api
- 类型: REST API
- 核心功能: 用户 CRUD 操作

## 功能需求
- 创建用户
- 查询用户
- 更新用户
- 删除用户

## 接口设计

| 方法 | 路径 | 描述 |
|------|------|------|
| POST | /users | 创建用户 |
| GET | /users | 获取用户列表 |
| GET | /users/{id} | 获取单个用户 |
| PUT | /users/{id} | 更新用户 |
| DELETE | /users/{id} | 删除用户 |

## 数据模型

| 字段 | 类型 | 必填 | 描述 |
|------|------|------|------|
| id | int | 是 | 用户 ID |
| username | str | 是 | 用户名 |
| email | str | 是 | 邮箱 |
| password | str | 是 | 密码 |

## 验收标准
- [ ] 创建用户成功
- [ ] 查询用户列表成功
- [ ] 更新用户成功
- [ ] 删除用户成功
```

## 配置

可在 `helix.yaml` 中配置：

```yaml
spec:
  llm_provider: anthropic
  model: claude-sonnet-4-20250514
  temperature: 0.7
```

## 关联技能

- `/helix-build` - 基于规格生成代码
- `/helix-verify` - 验证实现是否符合规格
