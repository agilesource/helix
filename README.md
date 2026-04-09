# Helix

> AI 时代软件工程方法论新范式

## 核心理念

> 当代码生成的边际成本趋近于零，架构的清晰度、需求的精确性、测试的完备性将成为人类创造价值的唯一分水岭。

Helix 是一个独立于特定 AI 智能体的软件工程工具框架，支持多种 AI Agent 作为执行引擎。

## 四大方法论融合

| 方法论 | 核心价值 | Helix 映射 |
|--------|----------|------------|
| 敏捷开发 | 快速响应变化 | `/spec` 规格驱动 |
| DevOps | 自动化全流程 | `/verify` 验证闭环 |
| 平台工程 | 封装能力 | 技能即服务 |
| 驾驭工程 | 人类掌舵，AI 执行 | 人类定义约束，AI 生成代码 |

## 安装

```bash
pip install helix-ai
```

或开发模式：

```bash
cd helix
pip install -e .
```

## 快速开始

### 1. 生成规格说明书

```bash
helix spec "我想做一个用户登录功能"
```

### 2. 生成代码骨架

```bash
helix build SPEC.md -o ./my-project
```

### 3. 验证代码

```bash
cd my-project
helix verify
```

## CLI 命令

| 命令 | 功能 |
|------|------|
| `helix spec <需求>` | 将需求转化为规格说明书 |
| `helix build <spec文件>` | 根据规格生成代码骨架 |
| `helix verify [路径]` | 运行静态检查、测试、验收 |
| `helix templates` | 列出可用模板 |
| `helix list-skills` | 列出所有技能 |
| `helix status` | 查看状态 |

## 支持的 AI 引擎

| 引擎 | 状态 |
|------|------|
| Claude Code | 🔜 计划中 |
| OpenClaw | 🔜 计划中 |
| OpenCode | 🔜 计划中 |
| Cursor | 🔜 计划中 |
| GitHub Copilot CLI | 🔜 计划中 |
| Gemini CLI | 🔜 计划中 |

## 项目结构

```
helix/
├── src/helix/
│   ├── core/           # 核心调度
│   ├── skills/         # 技能实现
│   │   ├── spec.py     # 规格生成
│   │   ├── build.py    # 代码骨架
│   │   └── verify.py   # 自动化验证
│   └── adapters/       # AI 引擎适配器
├── docs/               # 文档
└── tests/              # 测试
```

## 愿景、使命、价值观

见 [docs/brainstorming/VMV.md](docs/brainstorming/2026-04-09_Helix_VMV.md)

## 许可证

MIT
