# Helix /build 技能设计

> **版本**: v0.1
> **状态**: 详细设计
> **技能状态**: DRAFT

---

## 1. 技能概述

### 1.1 基本信息

| 属性 | 值 |
|------|-----|
| 名称 | `/build` |
| 命令 | `helix build <spec_file>` |
| 分类 | Execution (执行引擎) |
| 状态 | DRAFT (设计中) |
| 依赖 | `/spec` |

### 1.2 核心职责

读取规格说明书（Spec），生成代码骨架，为后续的代码填充做准备。

### 1.3 输入输出

```
输入: SPEC.md (规格说明书)
输出: 代码骨架 (models, api, tests)
```

---

## 2. 工作流程

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                             /build 工作流                                    │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  用户输入                                                                     │
│  helix build SPEC.md                                                        │
│       │                                                                     │
│       ▼                                                                     │
│  ┌─────────────┐                                                             │
│  │ Spec 解析   │ ◄── 解析 Markdown 规格                                      │
│  └─────────────┘                                                             │
│       │                                                                     │
│       ▼                                                                     │
│  ┌─────────────┐                                                             │
│  │ 依赖分析    │ ◄── 检查项目依赖、框架                                       │
│  └─────────────┘                                                             │
│       │                                                                     │
│       ▼                                                                     │
│  ┌─────────────┐                                                             │
│  │ 骨架生成    │ ◄── 生成 models, api, tests                                 │
│  └─────────────┘                                                             │
│       │                                                                     │
│       ▼                                                                     │
│  ┌─────────────┐                                                             │
│  │ 代码审查    │ ◄── 简单检查，标记需要手动填充的部分                         │
│  └─────────────┘                                                             │
│       │                                                                     │
│       ▼                                                                     │
│  输出: 代码骨架                                                               │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Spec 解析

### 3.1 支持的格式

- Markdown 文件 (`.md`)
- YAML 规格 (`.yaml`)

### 3.2 解析内容

| 章节 | 提取内容 |
|------|----------|
| 功能概述 | 功能名称、描述 |
| 功能需求 | 功能点列表、优先级 |
| 接口设计 | API 路径、请求/响应格式 |
| 数据模型 | 字段定义、类型 |
| 验收标准 | 测试用例 |

---

## 4. 骨架生成

### 4.1 支持的框架

| 框架 | 目录结构 |
|------|----------|
| Python/FastAPI | `models/`, `api/`, `tests/` |
| Python/Django | `models.py`, `views.py`, `tests/` |
| Node.js/Express | `models/`, `routes/`, `tests/` |

### 4.2 生成的文件类型

```
{project}/
├── models/
│   └── user.py           # 数据模型
├── api/
│   └── user.py           # API 路由
├── tests/
│   └── test_user.py      # 基础测试
├── requirements.txt      # 依赖
└── README.md             # 说明
```

---

## 5. CLI 接口设计

```bash
# 基本用法
helix build SPEC.md

# 指定输出目录
helix build SPEC.md --output ./src

# 指定框架
helix build SPEC.md --framework fastapi

# 预览（不生成）
helix build SPEC.md --dry-run

# 查看生成计划
helix build SPEC.md --plan
```

---

## 6. 核心模块设计

### 6.1 SpecParser

```python
class SpecParser:
    """解析规格说明书"""

    def parse(self, spec_file: str) -> SpecDocument:
        """解析 Markdown 规格文件"""
        ...

    def extract_apis(self, doc: SpecDocument) -> List[APIEndpoint]:
        """提取 API 定义"""
        ...

    def extract_models(self, doc: SpecDocument) -> List[Model]:
        """提取数据模型"""
        ...
```

### 6.2 CodeGenerator

```python
class CodeGenerator:
    """代码生成器"""

    def __init__(self, framework: str = "fastapi"):
        self.framework = framework

    def generate(self, spec: SpecDocument) -> CodeSkeleton:
        """生成代码骨架"""
        ...

    def generate_model(self, model: Model) -> str:
        """生成模型代码"""
        ...

    def generate_api(self, api: APIEndpoint) -> str:
        """生成 API 代码"""
        ...

    def generate_test(self, test_case: TestCase) -> str:
        """生成测试代码"""
        ...
```

---

## 7. 模板系统

### 7.1 FastAPI 模型模板

```python
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class {{ model_name }}Base(BaseModel):
    {% for field in fields %}
    {{ field.name }}: {{ field.type }}{% if not field.required %} | None{% endif %}
    {% endfor %}

class {{ model_name }}({{ model_name }}Base):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
```

### 7.2 FastAPI 路由模板

```python
from fastapi import APIRouter, Depends, HTTPException
from typing import List
from . import models

router = APIRouter(prefix="/{{ domain }}", tags=["{{ domain }}"])

@router.get("", response_model=List[models.{{ model_name }}])
async def list_{{ domain }}():
    # TODO: 实现列表查询
    pass

@router.get("/{id}", response_model=models.{{ model_name }})
async def get_{{ domain }}(id: str):
    # TODO: 实现单个查询
    pass

@router.post("", response_model=models.{{ model_name }})
async def create_{{ domain }}(item: models.{{ model_name }}Create):
    # TODO: 实现创建
    pass
```

---

## 8. 人类干预点

| 节点 | 干预方式 |
|------|----------|
| 解析失败 | 显示错误，手动修正 Spec |
| 框架选择 | 询问或默认 |
| 字段类型 | 标记为 TODO，需手动确认 |
| 业务逻辑 | 标记为 TODO，需手动实现 |

---

## 9. 待讨论问题

1. [ ] **默认框架** — 默认 FastAPI 还是检测现有项目？
2. [ ] **覆盖策略** — 已有文件如何处理？覆盖/合并/跳过？
3. [ ] **AI 集成** — 是否接入 LLM 填充业务逻辑？

---

## 10. 下一步

确认设计方向后，实现：
1. SpecParser
2. CodeGenerator
3. CLI 命令
