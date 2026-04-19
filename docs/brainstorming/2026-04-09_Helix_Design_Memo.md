# Helix — AI Era Software Engineering Methodology New Paradigm

> **Version**: v0.1 (Design Discussion Memo)
> **Date**: 2026-04-09
> **Status**: Concept Design Phase

---

## 1. Core Philosophy

### Naming Origin

**Helix** — DNA Double Helix Structure

```
    Human            AI Agent
       ●─────────────●
      ╱ ╲           ╱ ╲
     ╱   ╲─────────╱   ╲
    ●─────╲       ╱─────●
          ╲─────╱
         Co-evolution
```

**Core Metaphor**: Human intelligence and AI capabilities co-evolving, like a DNA double helix — intertwining and mutually enhancing.

### Core Principles

1. **When code cost approaches zero, architectural clarity becomes the sole differentiator**
2. **Human at the helm, AI executes** — the core of Harness Engineering
3. **Methodology hybrid** — don't blindly follow a single method, combine as needed
4. **Automated verification loop** — every AI output undergoes dual verification

---

## 2. Methodology Foundation

### 2.1 Four Methodology Integration

| Methodology | Core Value | Helix Mapping |
|-------------|------------|---------------|
| Agile Development | Rapid response to change, short iterative delivery | `/spec` Spec-driven, rapid iteration |
| DevOps | Full process automation, efficiency-driven | `/verify` Verification pipeline |
| Platform Engineering | Encapsulate capabilities, reduce cognitive load | Skills as services, standardized encapsulation |
| Harness Engineering | Human steers, AI executes | Human defines Spec + constraints, AI executes |

### 2.2 Core Transformation of Harness Engineering

| Traditional Role | AI Era Role |
|------------------|-------------|
| Code Producer | Architect/Driver |
| Write code | Write specifications + define architectural constraints + build verification loops |

---

## 3. System Architecture

### 3.1 Four-Layer Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           Layer 4: Meta-Methodology                         │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐       │
│  │ Agile       │  │ DevOps      │  │ Platform    │  │ Harness     │       │
│  │ Principles  │  │ Philosophy  │  │ Engineering │  │ Engineering │       │
│  │ (Process)   │  │ (Delivery)  │  │ (Capability)│  │ (Role)      │       │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘       │
├─────────────────────────────────────────────────────────────────────────────┤
│                           Layer 3: Execution Engine                         │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐       │
│  │ /spec       │  │ /build      │  │ /verify     │  │ /ship       │       │
│  │ Spec-driven │  │ Intelligent │  │ Automated   │  │ Delivery &  │       │
│  │             │  │ Build       │  │ Verification│  │ Release     │       │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘       │
├─────────────────────────────────────────────────────────────────────────────┤
│                           Layer 2: Quality Assurance                       │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐       │
│  │ /review     │  │ /test       │  │ /audit      │  │ /gate       │       │
│  │ Code Review │  │ Intelligent │  │ Security    │  │ Quality     │       │
│  │             │  │ Testing     │  │ Audit       │  │ Gate        │       │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘       │
├─────────────────────────────────────────────────────────────────────────────┤
│                           Layer 1: Infrastructure                           │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐       │
│  │ /browse     │  │ /design     │  │ /learn      │  │ /checkpoint │       │
│  │ Browser     │  │ Design      │  │ Continuous  │  │ State       │       │
│  │ Control     │  │ Generation  │  │ Learning    │  │ Persistence │       │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘       │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 3.2 Claude Code Integration

```
┌────────────────────────────────────────────────────────────┐
│                     Helix (Main Controller)                │
│  ┌──────────────────────────────────────────────────────┐ │
│  │  Intent Recognition → Methodology Selection          │ │
│  │  → Skill Routing → Execution → Verification          │ │
│  └──────────────────────────────────────────────────────┘ │
│           ↓              ↓            ↓            ↓      │
│  ┌────────────┐   ┌────────────┐ ┌────────────┐ ┌───────┐ │
│  │ Claude Code│   │ MCP Servers│ │ Skills     │ │Tools  │ │
│  │ (Reasoning)│   │ (Extension)│ │ (Reuse)    │ │(Exec) │ │
│  └────────────┘   └────────────┘ └────────────┘ └───────┘ │
└────────────────────────────────────────────────────────────┘
```

---

## 4. Detailed Skill Design

### 4.1 Layer 1: Infrastructure (Existing Capabilities Enhanced)

| Skill | Current State | Upgrade Direction |
|-------|---------------|-------------------|
| `/browse` | GStack existing | Enhance E2E testing, visual regression |
| `/design` | GStack existing | Spec-driven design generation |
| `/learn` | GStack existing | Project knowledge graph + cross-project learning |
| `/checkpoint` | GStack existing | Cross-session state continuation + decision traceability |

### 4.2 Layer 2: Quality Assurance

| Skill | Function | Key Features |
|-------|----------|--------------|
| `/review` | Code Review | Spec-aligned review, architectural constraint checking |
| `/test` | Intelligent Testing | Spec-driven test generation, edge cases |
| `/audit` | Security Audit | Dependency audit, architectural audit, security scanning |
| `/gate` | Quality Gate | Multi-dimensional checks (optional) |

### 4.3 Layer 3: Execution Engine

| Skill | Function | Key Features |
|-------|----------|--------------|
| `/spec` | Spec-driven | Requirement → Structured specification |
| `/build` | Intelligent Build | Spec → Code skeleton → Implementation |
| `/verify` | Automated Verification | Unit/Integration/Regression automated loop |
| `/ship` | Release & Delivery | Automated release process |

### 4.4 Layer 4: Meta-Methodology Scheduler

```python
class HelixOrchestrator:
    """Automatically select appropriate methodology combination based on context"""

    def dispatch(self, intent: str, context: dict) -> Skill:
        # Intent recognition + context-aware = skill routing
        if intent.contains("requirement") or intent.contains("feature"):
            return self.select("spec")  # Agile principles
        elif intent.contains("deploy") or intent.contains("release"):
            return self.select("ship")  # DevOps philosophy
        elif intent.contains("encapsulate") or intent.contains("platform"):
            return self.select("platform")  # Platform Engineering
        elif intent.contains("architecture") or intent.contains("constraint"):
            return self.select("constrain")  # Harness Engineering
```

---

## 5. Project Structure

```
helix/
├── helix-core/           # Core orchestration engine
│   ├── orchestrator.py   # Methodology routing
│   ├── intent_parser.py  # Intent recognition
│   ├── context_manager.py # Context management
│   └── config.py         # Configuration management
├── skills/               # Skill layer
│   ├── spec/            # Spec-driven (new design)
│   ├── build/           # Intelligent build (new design)
│   ├── verify/          # Automated verification (new design)
│   ├── review/          # Code review (GStack enhanced)
│   ├── test/            # Intelligent testing (new design)
│   ├── audit/           # Security audit (CSO enhanced)
│   ├── gate/            # Quality gate (new design)
│   ├── ship/            # Release & delivery (GStack enhanced)
│   ├── browse/          # Browser control (existing)
│   ├── design/          # Design generation (existing)
│   ├── learn/           # Continuous learning (existing)
│   └── checkpoint/      # State persistence (existing)
├── integration/          # Integration layer
│   ├── claude_code.py   # Claude Code adapter
│   └── mcp.py           # MCP protocol adapter
├── knowledge/            # Knowledge base
│   ├── patterns/        # Pattern library
│   └── templates/       # Specification templates
└── docs/                # Documentation
    ├── method.md        # Methodology documentation
    └── skills/          # Skill documentation
```

---

## 6. Iteration Roadmap

### Phase 1: Infrastructure (Week 1-2)
- Integrate existing GStack skills
- Build basic orchestration framework

### Phase 2: Core Skills (Week 3-6)
- `/spec` Spec-driven skill
- `/build` Intelligent build skill
- `/verify` Verification loop

### Phase 3: Quality Assurance (Week 7-10)
- `/test` Intelligent testing
- `/review` Enhancement
- `/audit` Integration
- `/gate` Gatekeeper

### Phase 4: Integration & Optimization (Week 11-12)
- End-to-end testing
- Performance optimization
- Documentation improvement

---

## 7. Reference Resources

- **Methodology Documents**: `/Users/liantian/Library/Mobile Documents/iCloud~md~obsidian/Documents/Dev/Method/software_engineering_evolution_ai_era.md`
- **GStack**: https://github.com/garrytan/gstack
- **Superpowers**: https://github.com/obra/superpowers
- **Google Engineering**: GStack ETHOS.md

---

## 8. Open Questions

1. [ ] Should skill names uniformly use the `/` prefix?
2. [ ] Do we need to support custom skill plugins?
3. [ ] How to handle relationships with existing Claude Code Skills?
4. [ ] Internationalization (English/Chinese) support priority?
5. [ ] Do we need cloud collaboration capabilities?

---

**Next Discussion Topic**: Detailed design of `/spec` skill (requirement → specification transformation)

---

*Design discussion participants: Peter Cheng + Jarvis*
*2026-04-09*
