# GStack + Agent-Skills 融合改进计划

**版本**: v1.0
**日期**: 2026-04-07
**作者**: Jarvis (Quality Engineering Director)
**目标**: 以 GStack 为主体，融入 Agent-Skills 优势能力

---

## 一、现状分析

### GStack 优势 (保留)

| 能力 | 状态 | 说明 |
|------|------|------|
| browse 二进制 | ✅ 保留 | 100ms/命令 headless browser |
| design 二进制 | ✅ 保留 | GPT Image API 设计生成 |
| learnings 记忆系统 | ✅ 保留 | 跨会话学习，避免重复犯错 |
| checkpoint 检查点 | ✅ 保留 | 跨分支保存工作进度 |
| 20+ 专业技能 | ✅ 保留 | /review, /cso, /qa, /ship 等 |
| 8+ 平台支持 | ✅ 保留 | Claude Code, OpenClaw, Codex 等 |

### Agent-Skills 优势 (需融入)

| 能力 | 当前状态 | 融入方案 |
|------|---------|---------|
| Rationalizations 反理性化表格 | ❌ 缺失 | 新增到核心技能模板 |
| Verification 验证证据 | ⚠️ 部分 | 统一标准化 |
| 3 Agent Personas | ❌ 缺失 | 新增 specialist agents |
| Google 工程实践 | ⚠️ 分散 | 系统化整合 |
| Process 流程强制 | ⚠️ 弱 | 增强工作流 |

---

## 二、改进计划

### Phase 1: 技能模板增强 (1周)

#### 1.1 SKILL.md.tmpl 增加 Rationalizations 章节

**位置**: `~/.claude/skills/gstack/SKILL.md.tmpl`

**新增内容**:

```markdown
## Rationalizations (反理性化)

本技能常见借口及反驳：

| 借口 | 反驳 |
|------|------|
| "我稍后添加测试" | 测试是技能的一部分，没有测试=未完成 |
| "这个很简单，不需要验证" | 简单不等于正确，必须有证据 |
| "我先提交，后面再改" | Tech debt 必须有 explicit TODO，否则不接受 |
| "不会有问题的" | 假设不能替代验证 |
```

**实施**:
- [x] 修改 SKILL.md.tmpl 模板
- [x] 运行 `bun run gen:skill-docs` 重新生成
- [x] 验证所有技能包含此章节

#### 1.2 统一 Verification 输出格式

**位置**: 所有执行类技能

**新增要求**:

```markdown
## Verification (验证证据)

完成本技能必须提供：

- [ ] 命令输出 (test/build/lint)
- [ ] 截图或日志 (如适用)
- [ ] 指标 (如: 测试覆盖率、性能数字)
- [ ] 状态: DONE | BLOCKED | NEEDS_CONTEXT
```

**实施**:
- [x] 更新 /review 技能
- [x] 更新 /qa 技能
- [x] 更新 /ship 技能
- [x] 更新 /investigate 技能

---

### Phase 2: Agent Personas 引入 (2周)

#### 2.1 新增 3 个 Specialist Agents

| Agent | 角色 | 职责 |
|-------|------|------|
| **code-reviewer** | Senior Staff Engineer | 代码审查、质量把关 |
| **qa-engineer** | QA Specialist | 测试设计、bug 验证 |
| **security-auditor** | Security Engineer | 安全审计、漏洞扫描 |

**实现方式**:

```
~/.claude/skills/gstack/agents/
├── code-reviewer/
│   ├── SKILL.md          # 角色定义
│   └── prompts.yaml      # 审查 prompt
├── qa-engineer/
│   ├── SKILL.md
│   └── test-templates/   # 测试模板
└── security-auditor/
    ├── SKILL.md
    └── owasp-checklist.md
```

**实施**:
- [x] 创建 gstack-fusion/skills/ 目录结构
- [x] 实现 code-reviewer 技能
- [x] 实现 qa-engineer 技能
- [x] 实现 security-auditor 技能

#### 2.2 技能调度集成

在 `/autoplan` 中增加 persona 选择逻辑：

```
用户输入 → Intent 检测 → 选择最适合的 Agent Persona
- 代码审查需求 → code-reviewer
- 测试需求 → qa-engineer
- 安全需求 → security-auditor
```

---

### Phase 3: Google 工程实践整合 (2周)

#### 3.1 核心原则引入

在 ETHOS.md 中新增章节：

```markdown
## Google 工程实践

以下原则来自 Google 内部工程实践：

1. **Hyrum's Law**: 接口的每个用户都是潜在依赖者
2. **Beyonce Rule**: 只要在代码中出现过，就必须有测试
3. **Test Pyramid**: 单元测试 : 集成测试 : E2E = 70% : 20% : 10%
4. **Chesterton's Fence**: 移除前先理解为什么存在
5. **Shift Left**: 尽早测试，持续测试
6. **Trunk-Based Development**: 小步提交，避免长期分支
```

#### 3.2 检查清单整合

在 `/review` 中增加 Google 检查项：

| 检查项 | 来源 | 优先级 |
|--------|------|--------|
| 测试覆盖率 | Beyonce Rule | P1 |
| 接口变更影响 | Hyrum's Law | P1 |
| 边界条件 | Test Pyramid | P2 |
| 回滚计划 | Chesterton's Fence | P2 |

**实施**:
- [x] 在 ETHOS.md 中添加 6 大 Google 原则
- [x] 创建 GOOGLE_CHECKLIST.md 模板
- [x] 集成检查清单到 /review 技能
| 回滚计划 | Chesterton's Fence | P2 |

---

### Phase 4: 流程强制增强 (1周)

#### 4.1 技能执行门禁

在 `/ship` 中增加强制检查：

```
/ship 执行流程:

1. [强制] /code-reviewer → 必须通过
2. [强制] /qa → 必须无 P0/P1 问题
3. [可选] /cso → 安全扫描
4. [强制] Verification 证据齐全
5. [强制] Rationalizations 检查通过
```

#### 4.2 拦截器机制

创建 gstack-interceptor 工具：

```
~/.claude/skills/gstack/bin/gstack-interceptor

功能:
- 拦截非技能调用 (直接回答问题)
- 引导用户使用正确技能
- 记录未使用技能的流失率
```

**实施**:
- [x] 在 /ship 中增加 Ship Gate 门禁
- [x] 创建 gstack-interceptor 工具
- [x] 集成门禁到 /ship 技能

---

### Phase 5: 文档与培训 (1周)

#### 5.1 更新文档

- [x] 更新 README.md - 融合说明
- [x] 创建 MIGRATION.md - 从纯 GStack 迁移指南
- [ ] 录制技能使用教程 (可选)
- [ ] 创建最佳实践案例 (可选)

---

## 实施完成 ✅

所有 5 个 Phase 已完成！

| Phase | 状态 |
|-------|------|
| Phase 1: 技能模板增强 | ✅ 完成 |
| Phase 2: Agent Personas | ✅ 完成 |
| Phase 3: Google 工程实践 | ✅ 完成 |
| Phase 4: 流程强制增强 | ✅ 完成 |
| Phase 5: 文档与培训 | ✅ 完成 |

---

## 三、实施时间线

| 周次 | Phase | 任务 |
|------|-------|------|
| **Week 1** | Phase 1 | 技能模板增强 (Rationalizations + Verification) |
| **Week 2-3** | Phase 2 | Agent Personas 实现 |
| **Week 4-5** | Phase 3 | Google 工程实践整合 |
| **Week 6** | Phase 4 | 流程强制增强 |
| **Week 7** | Phase 5 | 文档与培训 |

**总周期**: 7 周

---

## 四、验收标准

### 功能验收

| 功能 | 验收条件 |
|------|---------|
| Rationalizations | 所有技能包含反理性化表格 |
| Verification | 每个技能输出标准化验证证据 |
| Agent Personas | 3 个新 agent 可正常调用 |
| Google 实践 | ETHOS.md 包含 6+ 原则 |
| 流程强制 | /ship 包含完整门禁 |

### 质量验收

- [ ] 所有技能通过 `bun test`
- [ ] 新模板生成的 SKILL.md 格式正确
- [ ] 新增 agent 调用延迟 < 2 秒

---

## 五、风险与缓解

| 风险 | 影响 | 缓解措施 |
|------|------|---------|
| 模板变更破坏现有技能 | 高 | 先在测试环境验证 |
| Agent Personas 响应质量 | 中 | 用现有 /review, /cso 兜底 |
| 用户学习成本增加 | 低 | 提供渐进式迁移指南 |

---

## 六、后续计划

融合完成后，可以：

1. **vs Agent-Skills**: 比对方多记忆系统 + 工具链
2. **vs 纯 GStack**: 比原来多流程强制 + 工程实践
3. **独特优势**: 唯一同时拥有"工具深度"和"流程强制"的 AI 工程框架

---

**签署**:
- **Jarvis** (Quality Engineering Director) - 2026-04-07
- 对齐 **GStack** 主体架构
- 融合 **Agent-Skills** 最佳实践
- 目标: 最强 AI 工程框架

---

*文档状态: v1.0 草稿*
*等待 Peter 审批后生效*
