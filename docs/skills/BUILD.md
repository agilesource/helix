# Helix /build Skill Design

> **Version**: v0.1
> **Status**: Detailed Design
> **Skill Status**: DRAFT

---

## 1. Skill Overview

### 1.1 Basic Information

| Attribute | Value |
|-----------|-------|
| Name | `/build` |
| Command | `helix build <spec_file>` |
| Category | Execution (Execution Engine) |
| Status | DRAFT (In Design) |
| Dependencies | `/spec` |

### 1.2 Core Responsibility

Read the specification (Spec), generate code skeleton, and prepare for subsequent code implementation.

### 1.3 Input/Output

```
Input: SPEC.md (Specification)
Output: Code skeleton (models, api, tests)
```

---

## 2. Workflow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                             /build Workflow                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  User Input                                                                   │
│  helix build SPEC.md                                                         │
│       │                                                                     │
│       ▼                                                                     │
│  ┌─────────────┐                                                             │
│  │ Spec Parsing│ ◄── Parse Markdown specification                          │
│  └─────────────┘                                                             │
│       │                                                                     │
│       ▼                                                                     │
│  ┌─────────────┐                                                             │
│  │ Dependency  │ ◄── Check project dependencies, framework                 │
│  │ Analysis    │                                                             │
│  └─────────────┘                                                             │
│       │                                                                     │
│       ▼                                                                     │
│  ┌─────────────┐                                                             │
│  │ Skeleton    │ ◄── Generate models, api, tests                           │
│  │ Generation  │                                                             │
│  └─────────────┘                                                             │
│       │                                                                     │
│       ▼                                                                     │
│  ┌─────────────┐                                                             │
│  │ Code Review │ ◄── Simple check, mark parts needing manual filling       │
│  └─────────────┘                                                             │
│       │                                                                     │
│       ▼                                                                     │
│  Output: Code Skeleton                                                       │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Spec Parsing

### 3.1 Supported Formats

- Markdown file (`.md`)
- YAML specification (`.yaml`)

### 3.2 Parsed Content

| Section | Extracted Content |
|---------|-------------------|
| Feature Overview | Feature name, description |
| Functional Requirements | Feature list, priority |
| Interface Design | API paths, request/response format |
| Data Model | Field definitions, types |
| Acceptance Criteria | Test cases |

---

## 4. Skeleton Generation

### 4.1 Supported Frameworks

| Framework | Directory Structure |
|-----------|---------------------|
| Python/FastAPI | `models/`, `api/`, `tests/` |
| Python/Django | `models.py`, `views.py`, `tests/` |
| Node.js/Express | `models/`, `routes/`, `tests/` |

### 4.2 Generated File Types

```
{project}/
├── models/
│   └── user.py           # Data model
├── api/
│   └── user.py           # API routes
├── tests/
│   └── test_user.py      # Basic tests
├── requirements.txt      # Dependencies
└── README.md             # Documentation
```

---

## 5. CLI Interface Design

```bash
# Basic usage
helix build SPEC.md

# Specify output directory
helix build SPEC.md --output ./src

# Specify framework
helix build SPEC.md --framework fastapi

# Preview (don't generate)
helix build SPEC.md --dry-run

# View generation plan
helix build SPEC.md --plan
```

---

## 6. Core Module Design

### 6.1 SpecParser

```python
class SpecParser:
    """Parse specification document"""

    def parse(self, spec_file: str) -> SpecDocument:
        """Parse Markdown specification file"""
        ...

    def extract_apis(self, doc: SpecDocument) -> List[APIEndpoint]:
        """Extract API definitions"""
        ...

    def extract_models(self, doc: SpecDocument) -> List[Model]:
        """Extract data models"""
        ...
```

### 6.2 CodeGenerator

```python
class CodeGenerator:
    """Code generator"""

    def __init__(self, framework: str = "fastapi"):
        self.framework = framework

    def generate(self, spec: SpecDocument) -> CodeSkeleton:
        """Generate code skeleton"""
        ...

    def generate_model(self, model: Model) -> str:
        """Generate model code"""
        ...

    def generate_api(self, api: APIEndpoint) -> str:
        """Generate API code"""
        ...

    def generate_test(self, test_case: TestCase) -> str:
        """Generate test code"""
        ...
```

---

## 7. Template System

### 7.1 FastAPI Model Template

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

### 7.2 FastAPI Route Template

```python
from fastapi import APIRouter, Depends, HTTPException
from typing import List
from . import models

router = APIRouter(prefix="/{{ domain }}", tags=["{{ domain }}"])

@router.get("", response_model=List[models.{{ model_name }}])
async def list_{{ domain }}():
    # TODO: Implement list query
    pass

@router.get("/{id}", response_model=models.{{ model_name }})
async def get_{{ domain }}(id: str):
    # TODO: Implement single query
    pass

@router.post("", response_model=models.{{ model_name }})
async def create_{{ domain }}(item: models.{{ model_name }}Create):
    # TODO: Implement create
    pass
```

---

## 8. Human Intervention Points

| Node | Intervention Method |
|------|---------------------|
| Parse failure | Display error, manually fix Spec |
| Framework selection | Ask or use default |
| Field types | Mark as TODO, need manual confirmation |
| Business logic | Mark as TODO, need manual implementation |

---

## 9. Open Discussion Issues

1. [ ] **Default framework** — Default to FastAPI or detect existing project?
2. [ ] **Overwrite strategy** — How to handle existing files? Overwrite/merge/skip?
3. [ ] **AI integration** — Should we integrate LLM to fill business logic?

---

## 10. Next Steps

After confirming design direction, implement:
1. SpecParser
2. CodeGenerator
3. CLI command
