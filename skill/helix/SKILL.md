---
name: helix
description: "AI Era Software Engineering Methodology - 使用 helix CLI 进行规范化软件开发 (spec→build→verify→ship)"
---

# Helix Skill

使用 Helix CLI 进行 AI 时代的软件工程开发。Helix 定义了标准化的软件开发工作流。

> **安装:** `pip install helix-ai` 或使用 `python -m helix.cli`

## 工作流

```
需求 → helix spec → SPEC.md → helix build → 代码 → helix verify → helix ship → 发布
```

## L1: 执行引擎

### 规格说明

```bash
helix spec "创建用户登录功能"
```

生成 `SPEC.md` 文件，包含功能需求、接口设计、验收标准。

### 代码生成

```bash
helix build SPEC.md -o ./my-project
```

根据规格说明生成代码骨架。

### 验证

```bash
cd my-project
helix verify
```

运行静态检查、单元测试、验收测试。

### 发布

```bash
helix ship
```

执行发布流程 (PR → merge → tag → deploy)。

## L2: 质量保证

### 代码审查

```bash
helix review
```

### 智能测试

```bash
helix test
```

### 安全审计

```bash
helix audit
```

### 质量门禁

```bash
helix gate
```

## L3: 基础设施

### 浏览器控制

```bash
helix browse <url>
```

### 设计生成

```bash
helix design "设计描述"
```

### 持续学习

```bash
helix learn
```

### 状态持久化

```bash
helix checkpoint
```

## 配置

可在 `helix.yaml` 中配置：

```yaml
llm_provider: anthropic
model: claude-sonnet-4-20250514
workspace: ./my-project
```

## 示例工作流

```bash
# 1. 创建规格
helix spec "实现用户管理 API，支持 CRUD 操作"

# 2. 生成代码
helix build SPEC.md -o ./user-api

# 3. 验证
cd user-api
helix verify

# 4. 发布
helix ship
```

---

*Helix v1.0.0 - AI Era Software Engineering Methodology*
