# GStack Fusion v0.7.0 规划

**版本**: v0.7.0
**规划日期**: 2026-05-11
**目标**: 融合 agent-skills (addyosmani) 和 mattpocock/skills

---

## 一、需求分析

### 1.1 三个 Skill 库对比

| 维度 | GStack (v1.31) | agent-skills (Addy) | mattpocock/skills |
|------|----------------|---------------------|-------------------|
| **Skill 数量** | 50+ | 20 | ~10 |
| **核心理念** | CEO/Eng Manager 视角 | Google 工程实践 | TDD/PRD 流程 |
| **优势** | 完整工具链、部署 | 规范流程、质量门禁 | TDD、PRD、调试 |
| **适用场景** | 创业公司、全栈 | 企业级项目 | 需求不明确时 |

### 1.2 缺失功能 (需从外部融合)

| 功能 | 来源 | 优先级 |
|------|------|--------|
| PRD 编写 | mattpocock | HIGH |
| TDD 循环 | mattpocock | HIGH |
| PRD → Issues | mattpocock | HIGH |
| Spec 驱动开发 | agent-skills | HIGH |
| CI/CD 流水线 | agent-skills | MEDIUM |
| Context Engineering | agent-skills | MEDIUM |
| 代码简化 | agent-skills | LOW |
| 代码架构改进 | mattpocock | MEDIUM |

### 1.3 重复技能 (需合并)

| 技能 | 来源1 | 来源2 | 解决方案 |
|------|-------|-------|----------|
| /review | GStack | agent-skills | 保留 GStack 版本 (更完善) |
| /ship | GStack | agent-skills | 保留 GStack 版本 |
| /test | agent-skills | mattpocock (TDD) | 融合为 /tdd |
| /plan | GStack | agent-skills | 保留 GStack plan-* 系列 |

---

## 二、v0.7.0 架构设计

### 2.1 新的 Skill 分类体系

```
skills/
├── planning/                 # 需求与规划
│   ├── office-hours/         # [GStack] YC 产品发现
│   ├── spec-driven/          # [NEW] agent-skills: Spec 优先
│   ├── write-prd/            # [NEW] mattpocock: PRD 编写
│   ├── prd-to-issues/        # [NEW] mattpocock: PRD 转 Issues
│   └── plan-*/               # [GStack] CEO/Eng/Design Review
│
├── architecture/             # 架构与设计
│   ├── design-review/        # [GStack] UI/UX 审查
│   ├── plan-eng-review/      # [GStack] 架构审查
│   └── improve-architecture/ # [NEW] mattpocock: 架构改进
│
├── implementation/           # 代码实现
│   ├── codex/                # [GStack] AI 编码 Agent
│   ├── review/               # [GStack] 代码审查
│   └── code-reviewer/        # [Agent-Skills] 高级工程师角色
│
├── quality/                  # 质量保证
│   ├── tdd/                  # [NEW] mattpocock: TDD 循环
│   ├── qa/                   # [GStack] 浏览器测试
│   ├── qa-engineer/          # [Agent-Skills] QA 工程师角色
│   └── code-simplify/        # [NEW] agent-skills: 代码简化
│
├── debugging/                # 调试与调查
│   ├── investigate/          # [GStack] 根因分析
│   └── diagnose/             # [NEW] mattpocock: 系统调试
│
├── process/                  # 流程与运维
│   ├── git-workflow/         # [NEW] agent-skills: Git 工作流
│   ├── ci-cd/                # [NEW] agent-skills: CI/CD
│   ├── retro/                # [GStack] 回顾
│   └── context-engineering/  # [NEW] agent-skills: 上下文工程
│
├── deploy/                   # 部署与发布
│   ├── ship/                 # [GStack] 带门禁发布
│   ├── canary/               # [GStack] 金丝雀部署
│   └── land-and-deploy/      # [GStack] 生产部署
│
└── security/                 # 安全
    ├── cso/                  # [GStack] 安全审计
    └── security-auditor/     # [Agent-Skills] 安全工程师角色
```

### 2.2 新增 Skills 详细说明

| Skill | 来源 | 描述 | 命令 |
|-------|------|------|------|
| spec-driven | agent-skills | 先写 spec 再写代码 | /spec |
| write-prd | mattpocock | 产品需求文档编写 | /write-prd |
| prd-to-issues | mattpocock | PRD 转换为 GitHub Issues | /prd-to-issues |
| tdd | mattpocock | 红-绿-重构 TDD 循环 | /tdd |
| diagnose | mattpocock | 系统化调试方法论 | /diagnose |
| improve-architecture | mattpocock | 代码架构改进建议 | /improve-architecture |
| code-simplify | agent-skills | 代码简化与清理 | /code-simplify |
| git-workflow | agent-skills | Trunk-based 开发 | /git-workflow |
| ci-cd | agent-skills | CI/CD 流水线配置 | /ci-cd |
| context-engineering | agent-skills | 上下文管理 | /context |

### 2.3 融合策略

1. **保留 GStack 核心**: 工具链、部署、调查等技能保持不变
2. **融合 agent-skills 流程**: 将 SDLC 阶段映射到现有结构
3. **补充 mattpocock 特色**: TDD、PRD、诊断等独特能力
4. **统一命令规范**: 避免冲突，保持一致性

---

## 三、实施计划

### Phase 1: 准备阶段 (Karen 执行)

- [ ] 获取 agent-skills 完整 skill 列表
- [ ] 获取 mattpocock/skills 完整 skill 列表
- [ ] 创建 skills/planning, skills/quality, skills/debugging 等新目录

### Phase 2: 融合阶段 (Karen 执行)

- [ ] 迁移/复制 10 个新 skills 到 gstack-fusion
- [ ] 合并重复技能 (review, ship)
- [ ] 创建分类目录结构

### Phase 3: 验证阶段 (Friday 验收)

- [ ] 检查所有 SKILL.md 格式
- [ ] 验证无重复/冲突
- [ ] 更新文档和版本号

---

## 四、验收标准

| 标准 | 说明 |
|------|------|
| Skill 数量 | 从 16 个增加到 26+ 个 |
| 分类完整 | 8 个分类各至少 1 个 skill |
| 无重复 | 同类技能无冲突 |
| 格式统一 | 所有 SKILL.md 可正常解析 |
| 文档同步 | README/CHANGELOG 更新 |

---

## 五、风险与对策

| 风险 | 对策 |
|------|------|
| 网络问题无法获取 skills | 使用 GitHub API 或等待 Karen 完成后补全 |
| Skill 命令冲突 | 统一命名规范，保留更完善版本 |
| 内容重复 | 评估后融合或标记废弃 |

---

*此规划由 Friday AI 创建，待 Peter 审批后执行*

## 六、Helix 整合 (v0.7.0 完成后)

**状态**: ✅ 已审批，等待执行

整合目标: 将 GStack-Fusion 整合到 Helix 品牌下，形成完整的 AI 软件工程框架。

### 整合内容

| 组件 | 来源 | 目标 |
|------|------|------|
| 50+ Skills | GStack-Fusion | Helix/skills/ |
| 方法论文档 | GStack-Fusion | Helix/docs/methodology/ |
| 设计系统 | Helix | 保留 |
| CLI 工具 | Helix | 保留 |

### 版本规划

| 版本 | 内容 | 状态 |
|------|------|------|
| v1.0.0 | Helix 原有 12 Skills | ✅ Stable |
| v1.1.0 | + GStack-Fusion v0.6.0 (16 skills) | ⏳ 等待 |
| v1.2.0 | + GStack-Fusion v0.7.0 (26+ skills) | ⏳ 等待 |

### 下一步

v0.7.0 完成后，开始 Helix 整合任务。
