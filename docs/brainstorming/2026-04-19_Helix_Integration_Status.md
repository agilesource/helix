# Helix 与 OpenClaw/Claude Code 集成状态分析

**分析日期:** 2026-04-19
**基于:** 之前讨论结论（嵌入模式，v1.1.0 实现 Adapter）

---

## 一、讨论结论回顾

### 架构定位

| 项目 | 定位 | 关系 |
|------|------|------|
| **Helix** | 方法论框架 | 定义"如何做" |
| **OpenClaw/Claude Code** | AI 引擎 | 执行者 |

### 嵌入模式

```
用户 → AI Engine (OpenClaw/Claude Code)
            ↓
       Helix Engine (方法论)
            ↓
       输出结果
```

### 版本规划

| 版本 | 功能 |
|------|------|
| **v1.0.0** | 基础功能完善，CLI 可用 |
| **v1.1.0** | EngineAdapter + 适配器实现 |

---

## 二、当前集成状态

### 代码分析

#### 基类 (adapters/base.py)

```python
class AIAdapter(ABC):
    @abstractmethod
    async def execute(self, request: AIRequest) -> AIResponse:
        pass

class ClaudeCodeAdapter(AIAdapter):
    async def execute(self, request: AIRequest) -> AIResponse:
        raise NotImplementedError("Claude Code adapter not implemented")  # ❌ 未实现

class OpenClawAdapter(AIAdapter):
    async def execute(self, request: AIRequest) -> AIResponse:
        raise NotImplementedError("OpenClaw adapter not implemented")  # ❌ 未实现
```

**状态:** 接口定义存在，但实现为 `NotImplementedError`

#### OpenClaw 适配器 (adapters/openclaw_adapter.py)

```python
class OpenClawAdapter(AIAdapter):
    async def execute(self, request: AIRequest) -> AIResponse:
        # 构建 openclaw 命令
        cmd = self._build_command(request)
        # 执行
        result = await asyncio.create_subprocess_exec(*cmd, ...)
```

**状态:** ⚠️ 有实现代码，但依赖 `openclaw exec` 命令

#### Claude Code 适配器 (adapters/claude_code_adapter.py)

```python
class ClaudeCodeAdapter(AIAdapter):
    async def execute(self, request: AIRequest) -> AIResponse:
        cmd = self._build_command(request)
        # claude -p <prompt> --model <model>
        result = await asyncio.create_subprocess_exec(*cmd, ...)
```

**状态:** ⚠️ 有实现代码，但依赖 `claude` CLI

---

## 三、集成状态总结

| 适配器 | 接口 | 实现 | 依赖 | 可用性 |
|--------|------|------|------|--------|
| **OpenClawAdapter** | ✅ | ⚠️ 部分 | `openclaw exec` | ❓ 需验证命令是否存在 |
| **ClaudeCodeAdapter** | ✅ | ⚠️ 部分 | `claude` CLI | ❓ 需验证 CLI 是否存在 |
| **AnthropicAdapter** | ✅ | ✅ | Anthropic API | ✅ 可用（需 API Key） |

### 关键问题

1. **命令不存在风险**
   - `openclaw exec` 命令是否存在于 OpenClaw CLI？
   - `claude` CLI 是否已安装？

2. **调用方式不匹配**
   - OpenClaw 实际调用方式可能是 `sessions_spawn` 而非 `exec`
   - Claude Code 实际调用方式可能需要 `--print` 模式

3. **v1.0.0 定位**
   - 根据讨论，v1.0.0 不包含适配器实现
   - 适配器延后到 v1.1.0

---

## 四、正确集成方案

### OpenClaw 集成

**当前尝试:**
```bash
openclaw exec "prompt" --model sonnet  # ❓ 命令可能不存在
```

**正确方式 (基于 OpenClaw 架构):**
```python
# 方式 1: Python API
from openclaw import OpenClaw
oc = OpenClaw()
result = await oc.run("prompt")

# 方式 2: sessions_spawn
# 通过 OpenClaw 的 sessions_spawn 工具调用
```

### Claude Code 集成

**当前尝试:**
```bash
claude -p "prompt" --model claude-sonnet-4-20250514
```

**正确方式:**
```bash
# Claude Code CLI
claude --print "prompt"  # 或 claude -p

# 或使用 Claude Code SDK (如果有)
```

---

## 五、v1.0.0 vs v1.1.0 职责划分

### v1.0.0 (当前)

| 功能 | 状态 |
|------|------|
| CLI 可用 | ✅ `helix spec/build/verify/ship` |
| Skills 实现 | ✅ 12 Skills |
| 测试覆盖 | ✅ 62% |
| 类型标注 | ✅ mypy 0 错误 |
| **Adapter 实现** | ❌ 延后到 v1.1.0 |

### v1.1.0 (下一步)

| 功能 | 计划 |
|------|------|
| EngineAdapter 协议完善 | 定义标准接口 |
| OpenClaw Adapter | 正确集成方式 |
| Claude Code Adapter | 正确集成方式 |
| 嵌入模式支持 | 作为 Skill 或直接调用 |

---

## 六、建议行动

### 短期 (v1.0.0 发布)

1. ✅ 保持 Adapter 接口预留
2. ✅ 不实现具体 Adapter
3. ✅ 专注于 CLI 独立使用

### 中期 (v1.1.0 开发)

1. 调研 OpenClaw 正确调用方式
   - 检查 `openclaw exec` 是否存在
   - 考虑使用 OpenClaw Python API

2. 调研 Claude Code 正确调用方式
   - 检查 `claude` CLI 是否可用
   - 考虑 `--print` 模式

3. 实现 EngineAdapter 协议
   - 统一接口定义
   - 支持异步调用
   - 支持流式响应

---

## 七、结论

### 当前状态

| 维度 | 状态 |
|------|------|
| **接口定义** | ✅ 完成 |
| **实现代码** | ⚠️ 存在但可能不可用 |
| **v1.0.0 目标** | ✅ 正确（不包含 Adapter 实现） |
| **v1.1.0 规划** | 📋 已规划 |

### 建议

1. **v1.0.0 发布时:** 明确标注 Adapter 为"预留接口，v1.1.0 实现"
2. **v1.1.0 开发前:** 先调研 OpenClaw/Claude Code 的正确调用方式
3. **集成方式:** 遵循嵌入模式，支持多种调用方式（CLI/API/SDK）

---

**分析完成时间:** 2026-04-19 17:30 CST
