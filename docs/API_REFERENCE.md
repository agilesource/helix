# GStack Fusion - API 参考文档

完整的技能命令和参数索引。

---

## 核心技能

### /review - 代码审查

**描述**: Pre-landing PR 审查。分析 diff，检测 SQL 安全、LLM 信任边界、竞态条件等问题。

**参数**: 无需参数

**触发词**:
- "review this PR"
- "code review"
- "pre-landing review"
- "check my diff"

**输出格式**:
```
Pre-Landing Review: N issues (X critical, Y informational)
[CRITICAL] (confidence: N/10) file:line — description
[INFORMATIONAL] (confidence: N/10) file:line — description
```

---

### /qa - QA 测试

**描述**: 完整 QA 测试循环。测试 web 应用，修复发现的 bug。

**参数**:

| 参数 | 类型 | 说明 |
|------|------|------|
| `--tier` | string | 测试层级: quick/standard/full |
| `--url` | string | 要测试的 URL |
| `--headless` | bool | 是否 headless (默认 true) |

**触发词**:
- "qa"
- "test this site"
- "find bugs"
- "test and fix"

**输出格式**:
```
QA Testing: N bugs found
[LEVEL] Component - Description
[AUTO-FIXED] Component — Fix applied
```

---

### /qa-only - QA 报告 (仅报告)

**描述**: 与 /qa 相同，但不修复任何问题，只生成报告。

**参数**: 同 /qa

---

### /ship - 发布工作流

**描述**: 完整发布流程。合并 base，分流测试，审查 diff，bump VERSION，更新 CHANGELOG，提交，推送，创建 PR。

**参数**: 无需参数

**触发词**:
- "ship"
- "deploy"
- "push to main"
- "create a PR"

**门禁检查**:
- ✅ 测试通过
- ✅ Linting 通过
- ✅ 类型检查通过
- ✅ Codex 审查通过

---

### /investigate - 调试调查

**描述**: 系统性调试，根因分析。四阶段：调查、分析、假设、实施。

**参数**: 无需参数

**触发词**:
- "debug this"
- "fix this bug"
- "why is this broken"
- "investigate this error"

**输出格式**:
```
Phase 1: 收集证据
Phase 2: 分析根因
Phase 3: 提出假设
Phase 4: 实施修复

ROOT CAUSE FOUND:
[原因描述]

Fix applied: [修复内容]
```

---

## 测试与性能

### /benchmark - 性能基准

**描述**: 性能回归检测。建立页面加载时间、Core Web Vitals、资源大小的基准。比较每次 PR 的变化。

**参数**:

| 参数 | 类型 | 说明 |
|------|------|------|
| `--baseline` | bool | 建立新基准 |
| `--compare` | bool | 与基准比较 |
| `--url` | string | 要测试的 URL |

**触发词**:
- "performance"
- "benchmark"
- "page speed"
- "lighthouse"
- "bundle size"

---

### /canary - 上线后监控

**描述**: 部署后监控。监控线上应用的控制台错误、性能回归、页面失败。定期截图，与基准对比。

**参数**:

| 参数 | 类型 | 说明 |
|------|------|------|
| `--duration` | int | 监控时长(分钟) |
| `--interval` | int | 检查间隔(秒) |

**触发词**:
- "monitor deploy"
- "canary"
- "post-deploy check"
- "watch production"

---

## 安全

### /cso - 首席安全官模式

**描述**: 基础设施优先的安全审计。扫描 secrets、依赖供应链、CI/CD 安全、LLM/AI 安全、OWASP Top 10、STRIDE 威胁建模。

**参数**:

| 参数 | 类型 | 说明 |
|------|------|------|
| `--mode` | string | 模式: daily/comprehensive |

**触发词**:
- "security audit"
- "cso"
- "security review"

**输出格式**:
```
SECURITY AUDIT REPORT
=====================
Critical: N
High: N
Medium: N
Low: N

Findings:
[级别] 文件:行号 — 描述
```

---

### /security-auditor - Agent Persona

**描述**: 安全审计 Agent Persona (Security Engineer 角色)。

---

## 设计

### /design-consultation - 设计咨询

**描述**: 设计咨询。理解产品，研究领域，提出完整设计系统(美学、字体、颜色、布局、间距、动画)。

**参数**: 无需参数

**触发词**:
- "design system"
- "brand guidelines"

---

### /design-shotgun - 设计生成

**描述**: 设计 shotgun。生成多个 AI 设计变体，打开对比板，收集结构化反馈，迭代。

**参数**: 无需参数

**触发词**:
- "explore designs"
- "show me options"
- "design variants"

---

### /design-review - 设计审查

**描述**: 设计 QA。发现视觉不一致、间距问题、层次问题、AI 风格问题，修复。迭代式修复并验证。

**触发词**:
- "audit the design"
- "visual QA"
- "check if it looks good"

---

### /design-html - HTML 生成

**描述**: 生成生产级 Pretext 原生 HTML/CSS。

**参数**: 无需参数

---

## 规划与审查

### /office-hours - YC Office Hours

**描述**: YC Office Hours。两种模式：
- **Startup mode**: 6 个forcing questions 暴露需求现实
- **Builder mode**: 设计思考头脑风暴

**参数**: 无需参数

**触发词**:
- "brainstorm this"
- "I have an idea"
- "help me think through"

---

### /plan-ceo-review - CEO 模式计划审查

**描述**: CEO/founder 模式计划审查。重新思考问题，找 10 星产品，挑战前提。4 种模式：
- SCOPE EXPANSION (梦想大)
- SELECTIVE EXPANSION (保持范围+精选扩展)
- HOLD SCOPE (最大 rigor)
- SCOPE REDUCTION (精简到本质)

**触发词**:
- "think bigger"
- "expand scope"
- "strategy review"

---

### /plan-eng-review - 工程计划审查

**描述**: Eng Manager 模式计划审查。锁定执行计划：架构、数据流、图表、边缘情况、测试覆盖、性能。

**触发词**:
- "review the architecture"
- "engineering review"

---

### /plan-design-review - 设计计划审查

**描述**: 设计师视角计划审查。评分 7 个设计维度，解释如何达到 10 分，修复计划。

**触发词**:
- "review the design plan"
- "design critique"

---

### /plan-devex-review - 开发者体验计划审查

**描述**: 开发者体验计划审查。探索开发者角色，与竞品基准，设计魔法时刻，跟踪摩擦点。

**触发词**:
- "DX review"
- "developer experience audit"
- "devex review"

---

### /autoplan - 自动审查管道

**描述**: 自动审查管道。运行完整 CEO、设计、工程、DX 审查，使用 6 个决策原则自动决策。

**触发词**:
- "auto review"
- "autoplan"
- "run all reviews"

---

## 学习与记忆

### /learn - 学习管理

**描述**: 管理项目学习。搜索、修剪、导出跨会话的 gstack 学习。

**参数**:

| 参数 | 类型 | 说明 |
|------|------|------|
| `add` | string | 添加学习 |
| `search` | string | 搜索学习 |

**触发词**:
- "what have we learned"
- "show learnings"

---

### /checkpoint - 检查点

**描述**: 保存和恢复工作检查点。捕获 git 状态、决策、剩余工作。

**参数**:

| 参数 | 类型 | 说明 |
|------|------|------|
| `save` | string | 保存检查点 |
| `restore` | string | 恢复检查点 |
| `list` | list | 列出检查点 |

**触发词**:
- "checkpoint"
- "save progress"
- "resume"

---

## 代码质量

### /health - 代码质量仪表盘

**描述**: 代码质量仪表盘。包装现有项目工具(类型检查、linter、测试、dead code)，计算加权分数，跟踪趋势。

**触发词**:
- "health check"
- "code quality"
- "run all checks"

---

### /codex - Codex CLI 集成

**描述**: OpenAI Codex CLI 包装。三种模式：
- **Code review**: 独立 diff 审查
- **Challenge**: 对抗模式尝试破坏代码
- **Consult**: 咨询 anything

**参数**:

| 参数 | 类型 | 说明 |
|------|------|------|
| `review` | - | 代码审查模式 |
| `challenge` | - | 对抗模式 |
| `consult` | - | 咨询模式 |

**触发词**:
- "codex review"
- "codex challenge"
- "ask codex"

---

## 部署

### /land-and-deploy - 合并并部署

**描述**: 合并 PR，等待 CI 和部署，通过 canary 检查验证生产。

**触发词**:
- "merge"
- "land"
- "deploy"

---

### /setup-deploy - 配置部署

**描述**: 配置 /land-and-deploy。检测部署平台(production URL, health check 端点)。

**触发词**:
- "setup deploy"
- "configure deployment"

---

## 文档

### /document-release - 文档更新

**描述**: 文档发布后更新。读取所有项目文档，交叉引用 diff，更新 README/ARCHITECTURE/CONTRIBUTING/CLAUDE.md。

**触发词**:
- "update the docs"
- "sync documentation"

---

## 其他

### /retro - 回顾

**描述**: 周工程回顾。分析 commit 历史、工作模式、代码质量指标。

**触发词**:
- "weekly retro"
- "what did we ship"

---

### /browse - 浏览器交互

**描述**: Headless 浏览器。导航任意 URL，交互元素，验证页面状态，diff 前后操作，截图。

**参数**:

| 参数 | 类型 | 说明 |
|------|------|------|
| `--url` | string | 导航到 URL |
| `--screenshot` | bool | 截图 |

---

### /pair-agent - 配对远程 AI

**描述**: 配对远程 AI agent 到你的浏览器。生成设置密钥。

**触发词**:
- "pair agent"
- "connect agent"
- "share browser"

---

### /gstack-upgrade - 升级工具

**描述**: 升级 gstack 到最新版本。

**触发词**:
- "upgrade gstack"
- "update gstack"

---

### /freeze - 限制编辑

**描述**: 限制编辑到指定目录。阻止在允许路径外编辑。

**参数**: 无需参数

**触发词**:
- "freeze"
- "restrict edits"

---

### /guard - 完整安全模式

**描述**: 完整安全模式。组合 /careful + /freeze。

**触发词**:
- "guard mode"
- "full safety"

---

### /careful - 安全提醒

**描述**: 破坏性命令安全提醒。

**触发词**:
- "be careful"
- "safety mode"

---

### /unfreeze - 解除冻结

**描述**: 清除冻结边界，允许所有目录编辑。

**触发词**:
- "unfreeze"
- "unlock edits"

---

## Agent Personas

### /code-reviewer

**描述**: 高级工程师角色 (Senior Staff Engineer)。

### /qa-engineer

**描述**: QA 专家角色 (QA Specialist)。

### /security-auditor

**描述**: 安全审计角色 (Security Engineer)。

---

## 状态输出格式

所有技能使用统一的状态格式：

| 状态 | 说明 |
|------|------|
| **DONE** | 成功完成 |
| **DONE_WITH_CONCERNS** | 完成但有用户应知道的问题 |
| **BLOCKED** | 无法继续，说明阻塞原因 |
| **NEEDS_CONTEXT** | 缺少继续所需信息 |

---

## 决策分类

| 分类 | 说明 |
|------|------|
| **Mechanical** | 明显正确的答案，自动决定 |
| **Taste** | 合理的人可能不同意，表面在最终 gate |
| **User Challenge** | 两个模型都认为用户方向需要改变 |

---

## 输出优先级

1. CRITICAL / P0
2. HIGH / P1
3. MEDIUM / P2
4. LOW / P3
5. INFORMATIONAL

---

*API 参考完成 - v1.0.0*
