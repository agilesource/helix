# API Reference

> Helix v1.0.0-rc.2

## Core Modules

### helix

Main package module.

```python
import helix

helix.__version__  # "1.0.0-rc.2"
helix.__status__   # "RC"
```

### Core Classes

#### HelixContext

Session and project context management.

```python
from helix.core.context import HelixContext

ctx = HelixContext()
ctx.start_session("/path/to/project")
ctx.add_memory("pattern", "insight", ["tag1", "tag2"])
summary = ctx.get_summary()
```

#### Intent

User intent representation.

```python
from helix.core.intent import Intent, IntentType

intent = Intent(
    type=IntentType.BUILD,
    raw_input="Build a login feature",
    confidence=0.9,
    entities={"feature": "login"},
    parameters={"output_dir": "./src"}
)
```

#### IntentType

Available intent types:

| Type | Layer | Description |
|------|-------|-------------|
| `SPEC` | Execution | Requirement to specification |
| `BUILD` | Execution | Specification to code |
| `VERIFY` | Execution | Automated verification |
| `SHIP` | Execution | Release & delivery |
| `REVIEW` | Quality | Code review |
| `TEST` | Quality | Intelligent testing |
| `AUDIT` | Quality | Security audit |
| `GATE` | Quality | Quality gate |
| `BROWSE` | Infrastructure | Browser control |
| `DESIGN` | Infrastructure | Design generation |
| `LEARN` | Infrastructure | Continuous learning |
| `CHECKPOINT` | Infrastructure | State persistence |

### Skills

#### Skill Base Class

All skills inherit from `helix.skills.base.Skill`.

```python
from helix.skills.base import Skill, SkillConfig, SkillResult, SkillCategory, SkillStatus

class MySkill(Skill):
    name = "my-skill"
    description = "My custom skill"
    category = SkillCategory.EXECUTION
    status = SkillStatus.STABLE

    async def execute(self, intent, context) -> SkillResult:
        return SkillResult(
            success=True,
            message="Done",
            data={"key": "value"}
        )
```

#### SkillConfig

```python
config = SkillConfig(
    auto_confirm=False,
    timeout_seconds=300,
    max_retries=3,
    verbose=False
)
```

#### SkillResult

```python
result = SkillResult(
    success=True,
    message="Operation completed",
    data={"output": "/path/to/output"},
    skill_name="my-skill",
    execution_time_ms=1500,
    artifacts={"file": "/path"},
    warnings=["Warning 1"],
    errors=["Error 1"]
)
```

### AI Engine

#### AIEngineManager

```python
from helix.engines.manager import AIEngineManager, EngineConfig

manager = AIEngineManager()

config = EngineConfig(
    name="claude",
    adapter=my_adapter,
    priority=100,
    enabled=True
)
manager.register_engine(config)

engine = manager.get_engine("claude")
response = await manager.execute(request, engine_name="claude")
```

#### AIRequest / AIResponse

```python
from helix.engines.manager import AIRequest, AIResponse

request = AIRequest(
    prompt="Hello, world!",
    model="claude-3",
    max_tokens=4096,
    temperature=0.7,
    system_prompt="You are helpful."
)

response = AIResponse(
    success=True,
    content="Hello!",
    model="claude-3",
    tokens_used=100,
    metadata={"usage": {...}}
)
```

### CLI Commands

```bash
# Core commands
helix --help                    # Show help
helix status                    # Show status
helix list-skills               # List all skills
helix version                   # Show version

# Execution commands
helix spec "requirement"        # Generate specification
helix build <spec-file>         # Build code
helix verify [path]             # Verify code
helix ship [options]            # Ship/Release

# Quality commands
helix review [path]             # Code review
helix test [path]               # Run tests
helix audit [path]              # Security audit
helix gate                      # Quality gate

# Infrastructure commands
helix browse <url>              # Browser control
helix design <description>      # Design generation
helix learn [command]           # Learning system
helix checkpoint [command]      # State management
```

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `HELIX_ENV` | Environment | `development` |
| `HELIX_LOG_LEVEL` | Log level | `INFO` |
| `ANTHROPIC_API_KEY` | Anthropic API key | - |
| `OPENAI_API_KEY` | OpenAI API key | - |

### Docker

```bash
# Build image
docker build -t helix:1.0.0-rc.2 .

# Run with docker-compose
docker-compose up -d

# Development mode
docker-compose --profile dev up
```

---

*Last updated: 2026-04-19*
