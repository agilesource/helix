# Helix /spec Skill Design

> **Version**: v0.1
> **Status**: Detailed Design
> **Skill Status**: DRAFT

---

## 1. Skill Overview

### 1.1 Basic Information

| Attribute | Value |
|-----------|-------|
| Name | `/spec` |
| Command | `helix spec "<requirement description>"` |
| Category | Execution (Execution Engine) |
| Status | DRAFT (In Design) |
| Dependencies | None |

### 1.2 Core Responsibility

Transform user's natural language requirement descriptions into structured specifications (Spec), providing clear input for subsequent skills like `/build` and `/verify`.

### 1.3 Input/Output

```
Input: "I want to build a user login feature"
Output: Structured specification (Markdown format)
```

---

## 2. Workflow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              /spec Workflow                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  User Input                                                                   │
│  "I want to build a user login feature"                                      │
│       │                                                                     │
│       ▼                                                                     │
│  ┌─────────────┐                                                             │
│  │ Intent Parsing│ ◄── Understand what type of feature user wants          │
│  └─────────────┘                                                             │
│       │                                                                     │
│       ▼                                                                     │
│  ┌─────────────┐                                                             │
│  │ Requirement │ ◄── Socratic questioning, clarify ambiguous parts         │
│  │ Clarification│    If requirement is clear enough, skip this step        │
│  │ (Optional)  │                                                             │
│  └─────────────┘                                                             │
│       │                                                                     │
│       ▼                                                                     │
│  ┌─────────────┐                                                             │
│  │ Template    │ ◄── Select appropriate template based on feature type    │
│  │ Selection   │                                                             │
│  └─────────────┘                                                             │
│       │                                                                     │
│       ▼                                                                     │
│  ┌─────────────┐                                                             │
│  │ Spec        │ ◄── Fill template, generate structured Spec               │
│  │ Generation  │                                                             │
│  └─────────────┘                                                             │
│       │                                                                     │
│       ▼                                                                     │
│  ┌─────────────┐                                                             │
│  │ Human       │ ◄── Display Spec, user can modify or confirm              │
│  │ Confirmation│                                                             │
│  └─────────────┘                                                             │
│       │                                                                     │
│       ▼                                                                     │
│  Specification Output                                                         │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Intent Parsing

### 3.1 Requirement Classification

User input requirements can be classified into the following types:

| Type | Keywords | Example |
|------|----------|---------|
| CRUD | create, add, delete, modify, manage | "Build a user management system" |
| API | API, service, REST, GraphQL | "Build a user API" |
| Algorithm | calculate, sort, search, optimize | "Implement a recommendation algorithm" |
| Integration | integrate, third-party | "Integrate Stripe payment" |
| UI | page, component, UI, frontend | "Build a login page" |
| Script | script, tool, CLI | "Build a data import script" |
| Infrastructure | deploy, CI/CD, config | "Configure CI/CD" |

### 3.2 Entity Extraction

Extract key entities from requirements:

```python
@dataclass
class ExtractedEntities:
    domain: str = ""        # Domain: user, order, payment...
    action: str = ""        # Action: login, query, create...
    entities: List[str] = [] # Entities involved: username, password, verification code...
    integrations: List[str] = [] # Third-party integrations
    constraints: List[str] = []  # Constraints
```

---

## 4. Socratic Questioning Mechanism

### 4.1 Trigger Conditions

Trigger Socratic questioning when any of the following conditions are met:

1. **Domain unclear** — "Build a management system" → "What type of management system?"
2. **Action unclear** → "Build a feature" → "What exactly is the feature?"
3. **User unclear** → "For users" → "Who is the target user?"
4. **Value unclear** → "Build a login" → "What can users do after logging in?"

### 4.2 Questioning Strategy

```
Requirement Clarity = f(domain_clear, action_clear, user_clear, value_clear)

if Requirement Clarity >= 0.8:
    Directly proceed to template filling
elif Requirement Clarity >= 0.5:
    Selective questioning (max 3 key questions)
else:
    Guided questioning (until clarity >= 0.7)
```

### 4.3 Question Library

| Missing Info | Question Template |
|--------------|-------------------|
| Domain | "What business domain does this feature belong to?" |
| User | "Can you describe the target user?" |
| Value | "What problem does this feature solve for users?" |
| Scale | "How many users are expected to use this feature?" |
| Integration | "Which third-party systems need integration?" |
| Platform | "Which platforms need to be supported (Web/iOS/Android)?" |
| Acceptance | "How do you determine this feature is complete?" |

---

## 5. Template System

### 5.1 Template Types

| Template Name | Applicable Type | Core Sections |
|---------------|-----------------|---------------|
| `crud` | CRUD Operations | Data Model, API Design, Business Logic |
| `api` | API Service | Interface Definition, Authentication, Error Handling |
| `algorithm` | Algorithm Implementation | Algorithm Description, Complexity Analysis, Test Cases |
| `integration` | Third-party Integration | Integration Scheme, Error Handling, Fallback Strategy |
| `ui` | Page/Component | Interaction Design, State Definition, Responsive |
| `script` | Script Tool | Usage Scenario, Parameter Definition, Output Format |
| `infrastructure` | Infrastructure | Environment Requirements, Configuration, Deployment |

### 5.2 Template Structure

```markdown
# {Feature Name}

## 1. Feature Overview
{One sentence explaining what this does}

## 2. User Story
As a [role], I want [feature], so that [value]

## 3. Functional Requirements

### 3.1 Core Features
| # | Feature | Priority | Acceptance Criteria |
|---|---------|----------|---------------------|
| 1 |         | P0       |                    |

### 3.2 Edge Features
| # | Feature | Priority | Acceptance Criteria |
|---|---------|----------|---------------------|
| 1 |         | P1       |                    |

## 4. Non-Functional Requirements
- Performance:
- Security:
- Compatibility:

## 5. Interface Design
### 5.1 API
| Method | Path | Input | Output |
|--------|------|-------|--------|
|        |      |       |        |

### 5.2 Data Model
| Field | Type | Required | Description |
|-------|------|----------|-------------|
|        |      |          |             |

## 5. Acceptance Criteria (AC)
- [ ] Scenario 1: ...
- [ ] Scenario 2: ...

## 6. Edge Cases
- Edge case 1: ...
- Edge case 2: ...

## 7. Technical Constraints
- Dependencies: ...
- Limitations: ...

## 8. Risks and Dependencies
- Risks: ...
- Dependencies: ...
```

---

## 6. Human Confirmation

### 6.1 Confirmation Nodes

```
User Input → Intent Parsing ─┐
                            ▼
                   Requirement Clarification (Optional)
                            │
                            ▼
                   Template Selection ─┐
                            ▼
                   Fill Spec
                            │
                            ▼
                   Display to User ───────► Confirm / Modify / Cancel
                            │
                            ▼
                   Complete
```

### 6.2 Confirmation Options

| Option | Action |
|--------|--------|
| Confirm (Y) | Save Spec, proceed to next step |
| Modify (M) | Edit specific sections |
| Cancel (C) | Terminate, keep draft |

### 6.3 Modification Mode

User can specify modification scope:
- `spec edit section:<section_name>` — Modify specific section
- `spec edit item:<number>` — Modify specific requirement item
- `spec edit` — Open full editor

---

## 7. CLI Interface Design

```bash
# Basic usage
helix spec "I want to build a user login feature"

# With options
helix spec "I want to build a user login feature" \
  --template crud \           # Specify template
  --no-confirm \              # Skip confirmation
  --output spec.md \          # Output file
  --context .                 # Project context

# Interactive mode
helix spec                    # Enter interactive questioning

# View templates
helix spec templates          # List all templates

# Validate Spec
helix spec validate spec.md   # Validate specification
```

---

## 8. Configuration Files

### 8.1 Project-Level Config `.helix/spec.yaml`

```yaml
spec:
  # Default template
  default_template: crud

  # Auto-confirm mode
  auto_confirm: false

  # Template path
  template_dir: .helix/templates

  # Socratic questioning strategy
  socratic:
    max_questions: 5
    confidence_threshold: 0.7
```

### 8.2 Global Config `~/.helix/config.yaml`

```yaml
spec:
  # Preferred AI engine
  engine: claude_code

  # Output format
  default_format: markdown

  # Auto-learning
  learn_from_history: true
```

---

## 9. Open Discussion Issues

1. [ ] **Socratic questioning depth** — How deep should we go? Should we limit question rounds?

2. [ ] **Number of templates** — Are 7 templates enough? Do we need language/framework-specific subdivision?

3. [ ] **Confirmation mode** — Default confirm or default generate directly?

4. [ ] **Multi-round conversation** — Should we support adding new requirements after Spec generation?

5. [ ] **AI generation vs template filling** — Which parts use LLM generation, which use template filling?

6. [ ] **Project integration** — Do we need to read existing code to understand project context?

---

## 10. Next Steps

After confirming the design direction, implement:
1. Intent parser
2. Template system
3. Socratic questioner
4. CLI interface
