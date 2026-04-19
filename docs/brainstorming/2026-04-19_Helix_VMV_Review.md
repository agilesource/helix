# Project Helix VMV Review & 对齐报告

**审查日期:** 2026-04-19
**审查者:** Friday
**基于讨论:** Neo vs Helix 核心定位区分

---

## 一、当前 VMV 审查

### Vision 审查

**当前 Vision:**
> Build the software engineering operating system for human-AI co-evolution

**问题诊断:**

| 问题 | 严重度 | 说明 |
|------|--------|------|
| ⚠️ 定位模糊 | 中 | "Operating System" 容易与 Agent 本体混淆 |
| ⚠️ 与 Neo 重合 | 中 | "Human-AI co-evolution" 也是 Neo 的愿景 |
| ❌ 核心价值不突出 | 高 | 未强调"方法论"本质 |

**结论:** 需要重新定位，突出"方法论框架"本质。

---

### Mission 审查

**当前 Mission:**
> Create the most advanced software engineering toolchain in the AI era through the power of four methodologies

**问题诊断:**

| 问题 | 严重度 | 说明 |
|------|--------|------|
| ⚠️ "Toolchain" 误导 | 中 | 工具链 ≠ 方法论 |
| ✅ 四方法论整合 | 好 | 这是 Helix 的核心价值 |
| ⚠️ 未提及"流程规范" | 中 | 缺少方法论的核心产出 |

**结论:** 需要强调"流程规范"和"方法论框架"。

---

### Values 审查

**当前 5 个 Values:**
1. Human at the Helm ✅
2. Quality Obsessed ✅
3. Evolve Gradually ✅
4. Open Collaboration ✅
5. Tools Serve Humans ✅

**结论:** Values 基本正确，但需要增加"方法论独立性"原则。

---

## 二、VMV 重新对齐

### 2.1 Vision 重定义

**原 Vision:**
> Build the software engineering operating system for human-AI co-evolution

**新 Vision:**
> **成为 AI 时代的软件工程方法论标准**

**定义 AI 时代软件开发的"如何做"，而不是"谁来做"。**

**对齐理由:**
- 明确"方法论"本质
- 与 Neo 的"Agent 本体"定位区分
- 强调"标准"价值（工程标准、流程标准）

---

### 2.2 Mission 重定义

**原 Mission:**
> Create the most advanced software engineering toolchain in the AI era through the power of four methodologies

**新 Mission:**
> **通过四方法论融合，定义 AI 时代的软件工程流程规范**

1. **继承** — 吸收 Agile、DevOps、Platform Engineering、Harness Engineering 精华
2. **定义** — 建立 spec→build→verify→ship 的标准工作流
3. **验证** — 构建自动化的验证循环，确保流程执行
4. **赋能** — 让任何 AI Agent 都能遵循规范化流程开发

**对齐理由:**
- "流程规范"替代"工具链"
- 强调"定义标准"而非"创建工具"
- 明确产出是方法论，不是 Agent

---

### 2.3 Values 重定义

**增加第 6 个 Value:**

### 6. Methodology Independence

**原则:** 方法论独立于执行者

- Helix 定义的是"如何做事"，不是"谁来做"
- 可被任何 AI Agent (Claude/OpenClaw/Cursor) 采用
- 与 Agent 本体项目 (如 Project Neo) 平行发展
- 不依赖特定 Agent 的能力实现

---

## 三、对齐后的完整 VMV

### Vision

**成为 AI 时代的软件工程方法论标准**

定义 AI 时代软件开发的"如何做"，让规范化流程成为人机协作的基础。

---

### Mission

**通过四方法论融合，定义 AI 时代的软件工程流程规范**

1. **继承** — 吸收半世纪软件工程方法论精华
2. **定义** — 建立 spec→build→verify→ship 标准工作流
3. **验证** — 构建自动化验证循环
4. **赋能** — 让任何 AI Agent 都能遵循规范化流程

---

### Values

| 价值观 | 原则 | 与 Neo 区分 |
|--------|------|-------------|
| **1. Human at the Helm** | AI 执行，人类决策 | Neo: Agent 做决策 |
| **2. Quality Obsessed** | 质量是唯一壁垒 | Neo: 质量是护栏能力 |
| **3. Evolve Gradually** | 持续迭代演化 | Neo: 自主学习进化 |
| **4. Open Collaboration** | 开放协作 | Neo: 独立发展 |
| **5. Tools Serve Humans** | 工具服务人类 | Neo: Agent 服务人类 |
| **6. Methodology Independence** | 方法论独立于执行者 | Neo: Agent 是执行者 |

---

## 四、下一步迭代计划

### Phase 1: 核心框架完善 (2-3 周)

| 任务 | 优先级 | 预估 | 产出 |
|------|--------|------|------|
| EngineAdapter 接口定义 | P0 | 2天 | 引擎适配协议 |
| OpenClaw Adapter 实现 | P0 | 3天 | 首个可用适配器 |
| Claude Code Adapter 实现 | P1 | 3天 | 第二适配器 |
| /spec LLM 增强 | P1 | 2天 | 智能需求分析 |
| /verify 完善 | P1 | 2天 | 自动化验证 |
| 测试覆盖 >60% | P1 | 3天 | 质量保障 |

### Phase 2: 方法论标准化 (3-4 周)

| 任务 | 优先级 | 预估 | 产出 |
|------|--------|------|------|
| 7 阶段工作流文档化 | P1 | 3天 | 方法论白皮书 |
| 验证循环标准化 | P1 | 2天 | 验证规范 |
| 最佳实践库 | P2 | 3天 | 示例集合 |
| 企业部署指南 | P2 | 2天 | 部署文档 |

### Phase 3: 生态建设 (4-6 周)

| 任务 | 优先级 | 预估 | 产出 |
|------|--------|------|------|
| 社区贡献指南 | P2 | 2天 | CONTRIBUTING.md |
| 技能扩展框架 | P2 | 3天 | 插件系统 |
| 培训认证体系 | P3 | 5天 | 培训材料 |

---

## 五、与 Project Neo 的边界确认

| 维度 | Helix | Neo |
|------|-------|-----|
| **本质** | 方法论 | Agent |
| **产出** | 流程规范 | 运行系统 |
| **用户** | 开发团队 | Agent 使用者 |
| **整合方式** | 可选采用 | 独立运行 |
| **依赖关系** | 无 | 无 |

**边界原则:** Helix 不依赖 Neo，Neo 不依赖 Helix。两者可独立使用，也可组合使用。

---

## 六、VMV 更新建议

建议将本报告的 VMV 修订更新到：

1. `docs/brainstorming/2026-04-09_Helix_VMV.md` → v2.0
2. `README.md` 中更新 Vision/Mission 描述
3. `CHANGELOG.md` 记录 VMV 修订

---

**报告完成时间:** 2026-04-19 12:05 CST
