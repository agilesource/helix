# Project Helix - 版本迭代规划 (v0.5.0 ~ v1.0.0)

> 基于 VMV (Vision, Mission, Values) 和 Design Memo 的对齐
> 日期: 2026-04-10
> 状态: 规划中

---

## 一、愿景对齐回顾

### Vision (愿景)
**Build the software engineering operating system for human-AI co-evolution**

### Mission (使命)
Create the most advanced software engineering toolchain in the AI era through the power of four methodologies:
1. **Inherit** — 继承半个世纪的最佳工程实践
2. **Integrate** — 整合 GStack、Google、Superpowers 工作流
3. **Innovate** — 创新融合，构建前所未有的工作方式
4. **Empower** — 赋能每个开发者

### Values (价值观)
1. **Human at the Helm** — AI 是执行者，不是决策者
2. **Quality Obsessed** — 质量是唯一竞争壁垒
3. **Evolve Gradually** — 持续迭代，拒绝完美主义
4. **Open Collaboration** — 开放协作，集体智慧
5. **Tools Serve Humans** — 工具服务人类，不是技术炫技

---

## 二、设计架构回顾

### 四层架构

| Layer | Name | Skills | Status |
|-------|------|--------|--------|
| **L4** | Meta-Methodology | 方法论调度 | 待实现 |
| **L3** | Execution Engine | /spec, /build, /verify, /ship | ✅ v0.3.0 |
| **L2** | Quality Assurance | /review, /test, /audit, /gate | 部分 ✅ |
| **L1** | Infrastructure | /browse, /design, /learn, /checkpoint | 待集成 |

### 已实现 Skills

| Skill | Layer | 说明 | 版本 |
|-------|-------|------|------|
| /spec | L3 | 需求 → 规格说明书 | ✅ |
| /build | L3 | 规格 → 代码框架 | ✅ |
| /verify | L3 | 自动化验证 | ✅ |
| /ship | L3 | 发布与交付 | ✅ |
| /review | L2 | 代码审查 | ✅ |
| /qa | L2 | 测试自动化 (≈/test) | ✅ |
| /learn | L1 | 持续学习 | GStack (未集成) |
| /checkpoint | L1 | 状态持久化 | GStack (未集成) |

### 缺失 Skills (Design Memo 规划)

| Skill | Layer | 说明 |
|-------|-------|------|
| /audit | L2 | 安全审计 |
| /gate | L2 | 质量门禁 |
| /browse | L1 | 浏览器控制 |
| /design | L1 | 设计生成 |

---

## 三、版本迭代规划

### v0.5.0 — QA & Security 完善

**主题**: 质量保证与安全

**目标**:
- 完成 /audit (安全审计) skill
- 完成 /gate (质量门禁) skill
- 增强 /review (代码审查) 功能

**功能**:

| Skill | 功能 | 特性 |
|-------|------|------|
| /audit | 安全审计 | 依赖审计、架构审计、漏洞扫描 |
| /gate | 质量门禁 | 多维度检查、可配置阈值 |
| /review 增强 | 高级审查 | 架构约束检查、Spec 对齐审查 |

**价值对齐**:
- Quality Obsessed — 质量是竞争壁垒
- Human at the Helm — 人类定义约束，AI 执行

---

### v0.6.0 — Infrastructure 集成

**主题**: 基础设施层集成

**目标**:
- 集成 GStack /browse skill
- 集成 GStack /design skill
- 集成 GStack /learn skill
- 集成 GStack /checkpoint skill

**功能**:

| Skill | 功能 | 特性 |
|-------|------|------|
| /browse | 浏览器控制 | E2E 测试、视觉回归 |
| /design | 设计生成 | 规格驱动设计生成 |
| /learn | 持续学习 | 项目知识图谱 |
| /checkpoint | 状态持久化 | 跨会话状态延续 |

**价值对齐**:
- Evolve Gradually — 从现有能力集成开始
- Open Collaboration — 利用 GStack 已有能力

---

### v0.7.0 — AI Engine 深度集成

**主题**: AI 引擎深度集成

**目标**:
- Claude Code 完整集成
- OpenClaw 完整集成
- 多引擎切换与负载均衡
- 意图识别引擎 (Intent Recognition)

**功能**:

| 功能 | 说明 |
|------|------|
| Claude Code 桥接 | 工具执行、上下文注入 |
| OpenClaw 桥接 | 工作区管理、Action 执行 |
| 引擎选择器 | 根据任务类型选择最佳引擎 |
| 意图解析器 | 自然语言 → Skill 路由 |

**价值对齐**:
- Tools Serve Humans — 选择最适合的工具
- Human at the Helm — 人类控制 AI 行为

---

### v0.8.0 — Platform Engineering

**主题**: 平台化与扩展

**目标**:
- 插件市场雏形
- API 暴露 (REST/GraphQL)
- Web UI (Dashboard)
- CI/CD 集成

**功能**:

| 功能 | 说明 |
|------|------|
| 插件市场 | 插件发现、安装、评分 |
| REST API | 外部系统集成 |
| Dashboard | 项目状态可视化 |
| GitHub Actions | CI/CD pipeline 集成 |

**价值对齐**:
- Platform Engineering — 能力封装
- Open Collaboration — 开放生态

---

### v0.9.0 — 生产就绪

**主题**: 生产环境准备

**目标**:
- 性能优化
- 高可用架构
- 监控与告警
- 文档完善

**功能**:

| 功能 | 说明 |
|------|------|
| 性能优化 | 缓存、并发、懒加载 |
| 高可用 | 多实例部署、健康检查 |
| 监控 | 指标收集、告警 |
| 完整文档 | API 文档、使用指南 |

**价值对齐**:
- Quality Obsessed — 生产级质量
- Evolve Gradually — 稳步优化

---

### v1.0.0 — 里程碑发布

**主题**: 1.0 正式版

**目标**:
- 完整功能集
- 稳定版发布
- 社区启动

**功能**:

| 功能 | 说明 |
|------|------|
| 完整四层架构 | 所有 Design Memo 规划实现 |
| 生产稳定 | 经过验证的可靠版本 |
| 社区版本 | 开源发布、贡献者欢迎 |

**版本清单**:

| Layer | Skills | 状态 |
|-------|--------|------|
| L4 Meta-Methodology | 方法论调度 | ✅ |
| L3 Execution | /spec, /build, /verify, /ship | ✅ |
| L2 QA | /review, /qa, /audit, /gate | ✅ |
| L1 Infra | /browse, /design, /learn, /checkpoint | ✅ |

**价值对齐**:
- Vision — 软件工程操作系统
- Mission — AI 时代最先进工具链
- 所有价值观综合体现

---

## 四、版本依赖关系

```
v0.5.0 ──┬──> v0.6.0 ──┬──> v0.7.0 ──┬──> v0.8.0 ──┬──> v1.0.0
         │             │             │             │
    QA & Security  Infra集成    AI深度集成   平台化
```

---

## 五、迭代原则

基于 **VMV** 和 **Design Memo**:

1. **Human at the Helm** — 每个版本都增强人类对 AI 的控制
2. **Quality Obsessed** — QA 技能 (v0.5.0) 先于平台化
3. **Evolve Gradually** — 从基础设施到高级功能，层层递进
4. **Open Collaboration** — 集成 GStack 已有能力
5. **Tools Serve Humans** — 每个功能解决实际问题

---

## 六、开放问题 (来自 Design Memo)

| # | 问题 | 状态 | 解决版本 |
|---|------|------|----------|
| 1 | Skill 名称统一使用 `/` 前缀? | ✅ 已采用 | - |
| 2 | 支持自定义插件? | ✅ 已实现 | v0.4.0 |
| 3 | Claude Code Skills 关系? | 🔄 处理中 | v0.7.0 |
| 4 | i18n 支持? | ✅ 已完成 | v0.2.0 |
| 5 | 云协作能力? | 🔄 规划中 | v0.8.0 |

---

*规划参与者: Peter Cheng + Jarvis*
*2026-04-10*
