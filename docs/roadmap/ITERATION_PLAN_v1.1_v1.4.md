# Project Helix - 下一阶段迭代计划

> 基于 v1.0.0 评审反馈
> 日期: 2026-04-11
> 状态: 规划中

---

## 一、评审回顾

### 得分: 4.31/5.0 (86%)

| 维度 | 评分 | 权重 | 加权 |
|------|------|------|------|
| 架构 | ⭐⭐⭐⭐⭐ | 20% | 1.0 |
| 设计 | ⭐⭐⭐⭐⭐ | 20% | 1.0 |
| 功能 | ⭐⭐⭐⭐☆ | 20% | 0.9 |
| 实现 | ⭐⭐⭐⭐☆ | 15% | 0.85 |
| 质量 | ⭐⭐⭐⭐☆ | 10% | 0.85 |
| 发布 | ⭐⭐⭐⭐⭐ | 10% | 1.0 |
| 部署 | ⭐⭐⭐☆☆ | 5% | 0.7 |

---

## 二、改进优先级

### 🔴 高优先级 (影响生产使用)

| # | 问题 | 当前状态 | 目标 | 迭代版本 |
|---|------|---------|------|---------|
| 1 | 单元测试 | 0% | 70%+ | v1.1.0 |
| 2 | Docker支持 | 无 | 可用 | v1.1.0 |
| 3 | 类型标注 | 部分 | 完整(mypy通过) | v1.1.0 |

### 🟡 中优先级 (提升开发体验)

| # | 问题 | 当前状态 | 目标 | 迭代版本 |
|---|------|---------|------|---------|
| 4 | Web Dashboard | 无 | 基本可用 | v1.2.0 |
| 5 | GraphQL API | 无 | 基础CRUD | v1.2.0 |
| 6 | E2E测试 | 无 | 核心流程覆盖 | v1.2.0 |

### 🟢 低优先级 (长期增强)

| # | 问题 | 当前状态 | 目标 | 迭代版本 |
|---|------|---------|------|---------|
| 7 | 更多Adapter | 2个 | 5+ | v1.3.0 |
| 8 | 插件市场 | 无 | 基础版 | v1.3.0 |
| 9 | 云原生部署 | 无 | K8s/Helm | v1.4.0 |

---

## 三、详细迭代计划

### v1.1.0 — 质量与部署 (1-2周)

**主题**: 测试完善 + 容器化

**目标:**
- 单元测试覆盖率 70%+
- Docker镜像可用
- mypy类型检查通过

**功能:**

| 组件 | 功能 | 特性 |
|------|------|------|
| **测试框架** | pytest集成 | conftest, fixtures, mocks |
| **单元测试** | 核心模块覆盖 | core/, skills/, engines/ |
| **类型检查** | mypy集成 | strict模式, CI集成 |
| **Docker** | Dockerfile | Python基础镜像, 非root |
| **Docker** | docker-compose | API + Redis |

**测试覆盖率目标:**

```
src/helix/core/      → 80%+
src/helix/skills/    → 70%+
src/helix/engines/   → 80%+
src/helix/adapters/  → 60%+
```

**价值对齐:**
- Quality Obsessed — 测试是质量基石
- Tools Serve Humans — 一键部署

---

### v1.2.0 — DX增强 (2-4周)

**主题**: 开发者体验 + 可视化

**目标:**
- Web Dashboard可用
- GraphQL API
- E2E测试

**功能:**

| 组件 | 功能 | 特性 |
|------|------|------|
| **Dashboard** | Web UI | 技能状态、监控图表 |
| **Dashboard** | 实时日志 | WebSocket流式日志 |
| **Dashboard** | 配置管理 | Web界面配置 |
| **GraphQL** | API | 灵活查询, 减少over-fetching |
| **E2E测试** | Playwright | 核心CLI流程测试 |

**Dashboard功能:**

```
- 技能状态面板
- 性能监控图表
- 日志查看器
- 配置编辑器
- 健康检查
```

**价值对齐:**
- Evolve Gradually — DX持续优化
- Open Collaboration — 可视化促进协作

---

### v1.3.0 — 生态扩展 (1-2月)

**主题**: 生态系统 + 集成

**目标:**
- 更多AI Adapter
- 基础插件市场
- 集成增强

**功能:**

| 组件 | 功能 | 特性 |
|------|------|------|
| **Adapter** | OpenAI API | GPT-4o集成 |
| **Adapter** | Gemini CLI | Google AI |
| **Adapter** | Code CLI | OpenAI Codex |
| **Adapter** | Ollama | 本地模型 |
| **插件市场** | 索引服务 | 插件发现 |
| **插件市场** | 评分系统 | 用户反馈 |
| **集成** | GitHub App | PR自动审查 |
| **集成** | Slack Bot | 通知 webhook |

**Adapter接口:**

```python
class AIAdapter(ABC):
    name: str
    supported_models: List[str]

    @abstractmethod
    async def execute(self, request: AIRequest) -> AIResponse:
        pass

    @abstractmethod
    def is_available(self) -> bool:
        pass
```

**价值对齐:**
- Open Collaboration — 生态开放
- Tools Serve Humans — 更多选择

---

### v1.4.0 — 云原生 (2-3月)

**主题**: 云原生 + 企业级

**目标:**
- Kubernetes支持
- Helm Chart
- 企业特性

**功能:**

| 组件 | 功能 | 特性 |
|------|------|------|
| **K8s** | Deployment | 生产就绪配置 |
| **K8s** | Service | LoadBalancer |
| **K8s** | Ingress | 域名绑定 |
| **Helm** | Chart | 包管理 |
| **Terraform** | AWS/GCP/Azure | 一键部署 |
| **企业SSO** | OAuth2/SAML | 企业认证 |
| **审计日志** | 合规 | 完整操作记录 |
| **高可用** | 多副本 | 故障转移 |

**部署拓扑:**

```
┌─────────────────────────────────────────────────┐
│                  Load Balancer                  │
└─────────────────┬───────────────────────────────┘
                  │
        ┌─────────┼─────────┐
        ▼         ▼         ▼
    ┌───────┐ ┌───────┐ ┌───────┐
    │Helix  │ │Helix  │ │Helix  │
    │ Pod   │ │ Pod   │ │ Pod   │
    └───────┘ └───────┘ └───────┘
        │         │         │
        └─────────┼─────────┘
                  ▼
           ┌──────────┐
           │  Redis   │
           │ (State)  │
           └──────────┘
```

**价值对齐:**
- Quality Obsessed — 生产级质量
- Evolve Gradually — 稳步上云

---

## 四、迭代依赖关系

```
v1.1.0 ──┬──> v1.2.0 ──┬──> v1.3.0 ──┬──> v1.4.0
         │             │             │
    测试+Docker     Dashboard     生态+插件
                   GraphQL       云原生
```

---

## 五、迭代原则

基于 **VMV** 和评审反馈:

1. **Quality Obsessed** — v1.1.0把测试放第一位
2. **Human at the Helm** — Dashboard让人类更好掌控
3. **Evolve Gradually** — 每个版本独立可用
4. **Open Collaboration** — 插件市场鼓励社区贡献
5. **Tools Serve Humans** — 一键部署,开箱即用

---

## 六、开放问题

| # | 问题 | 状态 | 决策版本 |
|---|------|------|---------|
| 1 | Dashboard技术栈? (React/Vue/HTMX) | 🔄 讨论中 | v1.2.0 |
| 2 | 插件市场托管方式? (自建/GitHub) | 🔄 讨论中 | v1.3.0 |
| 3 | 云厂商优先级? (AWS/GCP/Azure) | 🔄 讨论中 | v1.4.0 |

---

## 七、发布清单检查

每次发布需确认:

- [ ] 单元测试 > 70%
- [ ] mypy检查通过
- [ ] Docker镜像构建成功
- [ ] Release Notes更新
- [ ] CHANGELOG更新
- [ ] GitHub Release创建

---

*规划参与者: Peter Cheng + Jarvis*
*2026-04-11*
