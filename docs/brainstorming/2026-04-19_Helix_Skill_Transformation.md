# Helix Skill 化改造方案

**日期:** 2026-04-19
**目标:** 将 Helix 改造为 OpenClaw/Claude Code Skill，像 GStack 一样使用

---

## 一、目标确认

### 当前状态 (v1.0.0)

```
Helix = Python Package + CLI
调用: helix spec/build/verify/ship
```

### 目标状态

```
Helix = OpenClaw/Claude Code Skill
调用: /helix-spec, /helix-build, /helix-verify, /helix-ship
```

---

## 二、改造方案

### 方案: 双模式架构

```
┌─────────────────────────────────────────────────────────────┐
│                    Helix v1.1.0                             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────────┐     ┌─────────────────┐               │
│  │   Skill 模式    │     │    CLI 模式     │               │
│  │ (内嵌到 Agent)  │     │  (独立使用)     │               │
│  └────────┬────────┘     └────────┬────────┘               │
│           │                       │                         │
│           └───────────┬───────────┘                         │
│                       ↓                                     │
│              ┌─────────────────┐                            │
│              │   Helix Core    │                            │
│              │ (共享 Python)   │                            │
│              └─────────────────┘                            │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 三、OpenClaw Skill 实现

### 目录结构

```
~/.openclaw/workspace/skills/helix/
├── SKILL.md                    # Skill 主文件
├── spec.md                     # /helix-spec
├── build.md                    # /helix-build
├── verify.md                   # /helix-verify
├── ship.md                     # /helix-ship
├── review.md                   # /helix-review
├── test.md                     # /helix-test
├── audit.md                    # /helix-audit
├── gate.md                     # /helix-gate
├── learn.md                    # /helix-learn
├── checkpoint.md               # /helix-checkpoint
├── design.md                   # /helix-design
└── browse.md                   # /helix-browse
```

### SKILL.md 示例

```markdown
---
name: helix
description: "AI Era Software Engineering Methodology - 7阶段工作流规范"
version: 1.1.0
author: Peter Cheng, Jarvis, Friday
tags: [ai, methodology, workflow, harness-engineering]
---

# Helix - AI 软件工程方法论

Helix 定义 AI 时代的软件工程工作流：**spec → build → verify → ship**

## 核心理念

当代码生成边际成本趋近于零时，架构清晰度和流程规范性成为核心价值。

## 可用 Skills

### 执行引擎 (L1)

| Skill | 描述 |
|-------|------|
| `/helix-spec` | 需求 → 结构化规格 |
| `/helix-build` | 规格 → 代码骨架 |
| `/helix-verify` | 自动验证循环 |
| `/helix-ship` | 发布流程 |

### 质量保证 (L2)

| Skill | 描述 |
|-------|------|
| `/helix-review` | 代码审查 |
| `/helix-test` | 智能测试生成 |
| `/helix-audit` | 安全审计 |
| `/helix-gate` | 质量门禁 |

### 基础设施 (L3)

| Skill | 描述 |
|-------|------|
| `/helix-browse` | 浏览器控制 |
| `/helix-design` | 设计生成 |
| `/helix-learn` | 持续学习 |
| `/helix-checkpoint` | 状态持久化 |

## 快速开始

```
/helix-spec "我需要实现用户登录功能"
/helix-build SPEC.md
/helix-verify
/helix-ship
```

## 方法论

Helix 融合四种方法论：
- **Agile**: 快速迭代 (spec-driven)
- **DevOps**: 全自动化 (verify loop)
- **Platform Engineering**: 能力封装 (Skills as Services)
- **Harness Engineering**: 人机协同 (Human steers, AI executes)
```

### spec.md 示例

```markdown
# /helix-spec

将用户需求转化为结构化规格说明。

## 使用方法

```
/helix-spec <需求描述>
```

## 示例

```
/helix-spec 我需要实现用户登录功能，支持邮箱和手机号登录
```

## 输出

生成 `SPEC.md` 文件，包含：
1. 功能概述
2. 用户故事
3. 功能需求
4. 非功能需求
5. API 设计
6. 数据模型
7. 验收标准
8. 边界情况

## 工作流

1. 分析用户需求
2. 识别实体和关系
3. 定义验收标准
4. 生成结构化文档
5. 询问澄清问题（如有必要）

## 注意事项

- 需求描述越详细，生成的规格越精确
- 如果信息不足，会提出澄清问题
- 生成的 SPEC.md 是后续 `/helix-build` 的输入
```

---

## 四、Claude Code Skill 实现

### 目录结构

```
~/.claude/skills/helix/
├── SKILL.md
├── spec.md
├── build.md
├── verify.md
├── ship.md
└── ... (其他 skills)
```

### SKILL.md (Claude Code 版本)

```markdown
---
name: helix
description: "AI Era Software Engineering Methodology"
version: 1.1.0
---

# Helix - AI 软件工程方法论

## Skills

### /helix-spec
需求 → 规格说明
生成结构化的 SPEC.md

### /helix-build
规格 → 代码
根据 SPEC.md 生成代码骨架

### /helix-verify
验证代码质量
运行静态检查 + 测试 + 验收

### /helix-ship
发布流程
自动化发布到 Git/GitHub

## 工作流

```
/helix-spec "需求" → /helix-build → /helix-verify → /helix-ship
```
```

---

## 五、实施计划

### Phase 1: OpenClaw Skill (v1.1.0)

| 任务 | 预估 |
|------|------|
| 创建 Skill 目录结构 | 0.5天 |
| 编写 12 个 Skill 文件 | 1天 |
| 测试 Skill 调用 | 0.5天 |
| 文档完善 | 0.5天 |

**总计:** 2.5天

### Phase 2: Claude Code Skill (v1.2.0)

| 任务 | 预估 |
|------|------|
| 创建 Claude Code Skill | 1天 |
| 测试兼容性 | 0.5天 |

**总计:** 1.5天

---

## 六、核心 Python 模块调整

### 当前结构

```
helix/
├── cli.py          # CLI 入口
├── core/           # 核心逻辑
└── skills/         # Skill 实现
```

### 调整后结构

```
helix/
├── cli.py          # CLI 入口 (保留)
├── core/           # 核心逻辑 (保留)
├── skills/         # Skill 实现 (保留)
├── skill/          # ← 新增: OpenClaw/Claude Code Skill 文件
│   ├── SKILL.md
│   ├── spec.md
│   ├── build.md
│   └── ...
└── __init__.py     # Python API 入口
```

---

## 七、使用对比

### 当前 (v1.0.0 CLI)

```bash
# 终端中
helix spec "实现登录功能"
helix build SPEC.md
helix verify
helix ship
```

### 改造后 (v1.1.0 Skill)

```
# OpenClaw/Claude Code 中
/helix-spec 实现登录功能
/helix-build
/helix-verify
/helix-ship
```

**用户体验更自然，无需切换到终端。**

---

## 八、决策请求

请确认是否采纳此方案：

- [ ] **是** - Helix 改造为 Skill 优先，CLI 保留作为备选
- [ ] **否** - 保持 CLI 为主，Skill 作为可选包装

---

**方案设计者:** Friday
**时间:** 2026-04-19 17:35 CST
