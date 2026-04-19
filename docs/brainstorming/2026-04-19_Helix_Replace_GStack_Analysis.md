# Helix v1.0.0 替代 GStack Fusion 可行性分析

**分析日期:** 2026-04-19
**分析者:** Friday

---

## 一、当前状态

### Jarvis 当前配置

| 项目 | 状态 |
|------|------|
| GStack Fusion | 已部署，作为 Claude Code Skill |
| 用途 | 小型 Harness Engineering 工具 |

### Helix v1.0.0 能力

| 能力 | 状态 |
|------|------|
| 12 Skills | ✅ 可用 |
| 测试覆盖率 | 62% |
| 类型安全 | ✅ mypy 0 错误 |
| CLI | ✅ 完整 |
| CLI 调用 | ✅ `helix spec/build/verify/ship` |

---

## 二、能力对比

### 核心功能覆盖

| 功能 | GStack Fusion | Helix v1.0.0 | 替代可行性 |
|------|---------------|--------------|------------|
| **需求分析** | ❌ 无 | ✅ `/spec` | ✅ 可替代 |
| **代码生成** | ❌ 无 | ✅ `/build` | ✅ 可替代 |
| **代码审查** | ✅ `/review` | ✅ `/review` | ✅ 可替代 |
| **测试生成** | ❌ 无 | ✅ `/test` | ✅ 可替代 |
| **安全审计** | ❌ 无 | ✅ `/audit` | ✅ 可替代 |
| **质量门禁** | ❌ 无 | ✅ `/gate` | ✅ 可替代 |
| **验证循环** | ⚠️ 部分 | ✅ `/verify` | ✅ 可替代 |
| **发布流程** | ❌ 无 | ✅ `/ship` | ✅ 可替代 |
| **持续学习** | ✅ learnings | ✅ `/learn` | ⚠️ 需适配 |
| **状态持久化** | ✅ checkpoint | ✅ `/checkpoint` | ⚠️ 需适配 |

### 部署方式对比

| 维度 | GStack Fusion | Helix v1.0.0 |
|------|---------------|--------------|
| **形态** | Claude Code Skill (Markdown) | Python Package + CLI |
| **调用方式** | `/gstack-xxx` | `helix xxx` 或 Python API |
| **依赖** | Claude Code 内置 | 独立安装 |
| **扩展性** | SKILL.md 扩展 | Skill 类扩展 |

---

## 三、替代方案

### 方案 A: CLI 调用模式

Jarvis 通过 CLI 调用 Helix：

```
用户 → Jarvis (Claude Code)
        ↓
      helix spec "需求描述"
        ↓
      Helix Engine
        ↓
      输出结果
```

**优点:**
- 独立进程，隔离性好
- 不需要修改 Helix
- 立即可用

**缺点:**
- 调用链较长
- 状态传递需序列化

### 方案 B: Python API 模式

Jarvis 直接调用 Helix Python API：

```python
# Jarvis 内部调用
from helix import HelixOrchestrator, HelixConfig

orchestrator = HelixOrchestrator(HelixConfig())
result = await orchestrator.run("我需要实现登录功能")
```

**优点:**
- 调用直接，性能好
- 状态共享方便
- 深度集成

**缺点:**
- 需要 Jarvis 支持 Python 导入
- 依赖管理复杂

### 方案 C: Claude Code Skill 包装器

将 Helix 包装为 Claude Code Skill：

```
~/.claude/skills/helix/SKILL.md
├── spec.md → 调用 helix spec
├── build.md → 调用 helix build
├── verify.md → 调用 helix verify
└── ship.md → 调用 helix ship
```

**优点:**
- 兼容 Claude Code 生态
- 用户体验一致
- 渐进式迁移

**缺点:**
- 需要维护包装层
- 功能映射可能有损耗

---

## 四、建议方案

### 推荐: 方案 C (Claude Code Skill 包装器)

**理由:**
1. 兼容现有 Jarvis 部署方式
2. 用户体验无缝切换
3. 可以渐进式迁移
4. 保持 Helix 独立性

### 实施步骤

#### Step 1: 创建 Helix Skill 包装器

```bash
mkdir -p ~/.claude/skills/helix
```

#### Step 2: 创建 SKILL.md

```markdown
---
name: helix
description: "AI Era Software Engineering Methodology - 7阶段工作流"
version: 1.0.0
---

# Helix - AI 软件工程方法论

## Skills

### /helix-spec
需求 → 规格说明
```bash
helix spec "$ARGUMENTS"
```

### /helix-build
规格 → 代码
```bash
helix build SPEC.md
```

### /helix-verify
验证代码质量
```bash
helix verify
```

### /helix-ship
发布流程
```bash
helix ship
```
```

#### Step 3: 迁移指南

| GStack Fusion 命令 | Helix 替代命令 |
|-------------------|---------------|
| `/gstack-review` | `/helix-review` 或 `helix review` |
| `/gstack-health` | `/helix-gate` |
| N/A | `/helix-spec` (新增) |
| N/A | `/helix-build` (新增) |
| N/A | `/helix-verify` (新增) |
| N/A | `/helix-ship` (新增) |

---

## 五、结论

### ✅ 可行性: 高

| 维度 | 评估 |
|------|------|
| 功能覆盖 | ✅ Helix 功能更完整 |
| 技术可行 | ✅ CLI/Skill 包装都可 |
| 迁移成本 | ⚠️ 需要创建包装层 |
| 用户影响 | ✅ 命令略有变化，但功能增强 |

### 建议

1. **优先级:** Helix v1.0.0 发布后立即实施
2. **方式:** 方案 C (Claude Code Skill 包装器)
3. **时机:** Milestone 4 完成后

---

**分析完成时间:** 2026-04-19 17:05 CST
