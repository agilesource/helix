"""
/spec Skill - Fallback (Rule-based)

Original rule-based specification generator (used when LLM unavailable)
"""

import asyncio
import re
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from enum import Enum

from helix.skills.base import Skill, SkillResult, SkillConfig, SkillCategory, SkillStatus
from helix.core.intent import Intent, IntentType
from helix.core.context import HelixContext


class RequirementType(Enum):
    """Requirement types"""

    CRUD = "crud"
    API = "api"
    ALGORITHM = "algorithm"
    INTEGRATION = "integration"
    UI = "ui"
    SCRIPT = "script"
    INFRASTRUCTURE = "infrastructure"
    GENERAL = "general"


@dataclass
class ExtractedEntities:
    """Entities extracted from requirements"""

    domain: str = ""
    action: str = ""
    entities: List[str] = field(default_factory=list)
    integrations: List[str] = field(default_factory=list)
    constraints: List[str] = field(default_factory=list)
    target_users: List[str] = field(default_factory=list)
    value_proposition: str = ""
    features: List[str] = field(default_factory=list)
    project_context: str = ""


class SpecSkillFallback(Skill):
    """Fallback specification generator (rule-based)"""

    name = "spec"
    description = "Transform requirements into structured specifications"
    category = SkillCategory.EXECUTION
    status = SkillStatus.DRAFT

    examples = [
        "I want to build a user login feature",
        "Create a user management API",
    ]

    TEMPLATE_DIR = ".helix/templates/spec"

    def __init__(self, config: Optional[SkillConfig] = None):
        super().__init__(config)
        self._templates: Dict[RequirementType, str] = {}

    def _do_initialize(self) -> None:
        """Load templates"""
        self._templates = {
            RequirementType.CRUD: self._crud_template(),
            RequirementType.API: self._api_template(),
            RequirementType.ALGORITHM: self._algorithm_template(),
            RequirementType.INTEGRATION: self._integration_template(),
            RequirementType.UI: self._ui_template(),
            RequirementType.SCRIPT: self._script_template(),
            RequirementType.INFRASTRUCTURE: self._infrastructure_template(),
            RequirementType.GENERAL: self._general_template(),
        }

    async def execute(self, intent: Intent, context: HelixContext) -> SkillResult:
        """Execute skill"""
        self.initialize()
        start_time = asyncio.get_event_loop().time()

        user_input = intent.raw_input

        # Step 1: Classify requirement
        req_type = self._classify_requirement(user_input)
        entities = self._extract_entities(user_input)

        # Step 2: Generate spec
        spec_content = self._generate_spec(user_input, req_type, entities, {})

        execution_time = int((asyncio.get_event_loop().time() - start_time) * 1000)

        return SkillResult(
            success=True,
            message="Specification generated (fallback mode)",
            data={
                "requirement_type": req_type.value,
                "entities": {
                    "domain": entities.domain,
                    "action": entities.action,
                },
                "spec_content": spec_content,
                "llm_used": False,
            },
            skill_name=self.name,
            execution_time_ms=execution_time,
            artifacts={"spec": spec_content},
        )

    def _classify_requirement(self, user_input: str) -> RequirementType:
        """Classify requirement type"""
        input_lower = user_input.lower()

        # Priority checks first - more specific patterns

        # API - service interfaces (check before CRUD)
        if any(kw in input_lower for kw in ["rest api", "api endpoint", "graphql api", "create api", "build api"]):
            return RequirementType.API
        if any(kw in input_lower for kw in ["api", "接口", "rest", "graphql", "endpoint"]) and any(kw in input_lower for kw in ["create", "build", "implement"]):
            return RequirementType.API

        # Integration - third party services (check early)
        if any(kw in input_lower for kw in ["integrate", "integration", "wechat", "alipay", "stripe", "oauth", "webhook", "sdk"]):
            return RequirementType.INTEGRATION

        # Notification (email, SMS, push) - treat as integration
        if any(kw in input_lower for kw in ["notification", "notify", "email", "sms", "push notification", "message"]):
            return RequirementType.INTEGRATION

        # Payment (before CRUD)
        if any(kw in input_lower for kw in ["payment", "支付", "billing", "checkout"]):
            return RequirementType.INTEGRATION

        # CLI/Script tools (before CRUD)
        if any(kw in input_lower for kw in ["cli tool", "command line", "bash script", "shell script"]):
            return RequirementType.SCRIPT
        if any(kw in input_lower for kw in ["script", "脚本", "cli", "command", "batch", "automation", "export", "import"]) and any(kw in input_lower for kw in ["tool", "工具"]):
            return RequirementType.SCRIPT

        # Infrastructure - DevOps (check early)
        if any(kw in input_lower for kw in ["deploy", "部署", "ci/cd", "ci ", " cd", "docker", "kubernetes", "k8s", "pipeline", "infrastructure"]):
            return RequirementType.INFRASTRUCTURE

        # CRUD - data management
        if any(kw in input_lower for kw in ["login", "登录", "注册", "auth", "认证", "register", "signin", "signup"]):
            return RequirementType.CRUD
        if any(kw in input_lower for kw in ["create", "添加", "delete", "modify", "管理", "crud", "add", "remove", "update", "edit"]):
            return RequirementType.CRUD
        if any(kw in input_lower for kw in ["management", "管理"]):
            return RequirementType.CRUD

        # Algorithm - computation
        if any(kw in input_lower for kw in ["algorithm", "算法", "recommend", "recommendation", "sorting", "searching", "search", "filter", "analyze"]):
            return RequirementType.ALGORITHM

        # UI - front-end
        if any(kw in input_lower for kw in ["page", "页面", "ui", "前端", "component", "button", "form", "modal", "dashboard", "layout", "screen"]):
            return RequirementType.UI

        return RequirementType.GENERAL

    def _extract_entities(self, user_input: str) -> ExtractedEntities:
        """Extract entities"""
        entities = ExtractedEntities()

        # Domain keywords mapping
        domain_keywords = {
            "user": ["user", "用户", "登录", "注册", "account", "账号", "profile", "权限", "permission", "role"],
            "order": ["order", "订单", "purchase", "购买", "checkout", "cart", "shopping"],
            "product": ["product", "商品", "产品", "item", "sku", "inventory"],
            "content": ["content", "内容", "文章", "post", "blog", "news", "article"],
            "payment": ["payment", "支付", "billing", "invoice", "refund"],
            "notification": ["notification", "通知", "message", "email", "sms", "push"],
            "analytics": ["analytics", "分析", "statistics", "metrics", "report", "dashboard"],
            "file": ["file", "文件", "upload", "download", "attachment", "image", "avatar"],
            "search": ["search", "搜索", "query", "filter"],
            "auth": ["auth", "认证", "oauth", "jwt", "token", "session", "sso"],
        }

        for domain, keywords in domain_keywords.items():
            if any(kw in user_input.lower() for kw in keywords):
                entities.domain = domain
                break

        # Extract action from common patterns
        action_keywords = {
            "create": ["create", "add", "new", "生成", "创建", "添加"],
            "read": ["get", "fetch", "list", "view", "查询", "获取", "查看"],
            "update": ["update", "edit", "modify", "修改", "编辑"],
            "delete": ["delete", "remove", "删除", "移除"],
            "login": ["login", "signin", "登录", "authenticate"],
            "logout": ["logout", "signout", "登出"],
            "search": ["search", "query", "find", "搜索", "查找"],
            "upload": ["upload", "上传"],
            "download": ["download", "下载"],
        }

        for action, keywords in action_keywords.items():
            if any(kw in user_input.lower() for kw in keywords):
                entities.action = action
                break

        # Chinese pattern: XX管理
        match = re.search(r'(\w+)管理', user_input)
        if match:
            entities.domain = match.group(1)

        # Extract target users
        if "admin" in user_input.lower() or "管理员" in user_input:
            entities.target_users = ["Administrator", "Admin"]
        elif "developer" in user_input.lower() or "开发者" in user_input:
            entities.target_users = ["Developer"]
        else:
            entities.target_users = ["End user"]

        return entities

    def _generate_spec(
        self,
        user_input: str,
        req_type: Any,  # Accept both string and enum
        entities: ExtractedEntities,
        clarifications: Dict[str, str]
    ) -> str:
        """Generate specification from template"""
        # Convert string to enum if needed
        if isinstance(req_type, str):
            try:
                req_type = RequirementType(req_type)
            except ValueError:
                req_type = RequirementType.GENERAL
        elif not isinstance(req_type, RequirementType):
            req_type = RequirementType.GENERAL

        template = self._templates.get(req_type)
        if not template:
            template = self._templates.get(RequirementType.GENERAL)

        function_name = self._infer_function_name(user_input)
        domain = entities.domain or "general"
        action = entities.action or "operation"

        spec = template.format(
            function_name=function_name,
            domain=domain,
            action=action,
            features=action,
            user_input=user_input,
            clarifications="N/A",
            target_users="End user",
            value_proposition="Meet business needs",
            project_context="",
        )

        return spec

    def _infer_function_name(self, user_input: str) -> str:
        """Infer function name"""
        cleaned = re.sub(r"^(I want to|我想|我要|帮我|create a|build a)\s*", "", user_input, flags=re.IGNORECASE)
        words = cleaned.split(" for ") or cleaned.split(" to ")
        if len(words) > 0:
            return words[-1].strip().title()
        return cleaned.strip().title()

    # Templates
    def _crud_template(self) -> str:
        return """# {function_name}

## 1. Feature Overview
{user_input}

## 2. User Story
As a {target_users}, I want to {features} {domain}, so that {value_proposition}.

## 3. Functional Requirements

### 3.1 Core Features (P0)
| # | Feature | Acceptance Criteria |
|---|---------|---------------------|
| 1 | {features} | Operation succeeds and returns correct result |
| 2 | Data Validation | Valid input succeeds, invalid shows clear error |
| 3 | Permission Control | Unauthorized users cannot execute |

### 3.2 Edge Features (P1)
| # | Feature | Acceptance Criteria |
|---|---------|---------------------|
| 1 | Batch Operations | Support batch processing |
| 2 | Data Export | Export to common formats |

## 4. Non-Functional Requirements
- **Performance**: Response time < 200ms
- **Security**: Sensitive data encrypted in transit
- **Compatibility**: Support major browsers/clients

## 5. API Design

### 5.1 API Endpoints
| Method | Path | Description |
|--------|------|-------------|
| GET | /api/{domain} | List {domain} |
| GET | /api/{domain}/{{id}} | Get single {domain} |
| POST | /api/{domain} | Create {domain} |
| PUT | /api/{domain}/{{id}} | Update {domain} |
| DELETE | /api/{domain}/{{id}} | Delete {domain} |

### 5.2 Data Model
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| id | UUID | Yes | Primary key |
| created_at | datetime | Yes | Creation time |
| updated_at | datetime | Yes | Update time |

## 6. Acceptance Criteria
- [ ] {features} operation completes successfully
- [ ] Invalid input shows clear error message
- [ ] Unauthorized operations are rejected
- [ ] Performance meets requirements
"""

    def _api_template(self) -> str:
        return """# {function_name}

## 1. Feature Overview
{user_input}

## 2. User Story
As a {target_users}, I need an API to {features} {domain}, so that {value_proposition}.

## 3. Functional Requirements
- [ ] API endpoint accepts requests
- [ ] Returns proper HTTP status codes
- [ ] Handles errors gracefully
- [ ] Supports required data formats

## 4. API Design
| Method | Path | Request | Response |
|--------|------|---------|----------|
| GET | /api/{domain} | - | List of {domain} |
| POST | /api/{domain} | {domain} data | Created {domain} |

## 5. Acceptance Criteria
- [ ] API responds with correct status codes
- [ ] Request/response format is correct
- [ ] Error handling works properly
"""

    def _algorithm_template(self) -> str:
        return """# {function_name}

## 1. Feature Overview
{user_input}

## 2. Functional Requirements
- [ ] Algorithm implements required functionality
- [ ] Handles edge cases
- [ ] Provides correct results

## 3. Algorithm Description
Describe the algorithm here:

## 4. Complexity Analysis
- Time Complexity: O(?)
- Space Complexity: O(?)

## 5. Test Cases
| Input | Expected Output |
|-------|-----------------|
|       |                 |

## 6. Acceptance Criteria
- [ ] Produces correct output for test cases
- [ ] Performance meets requirements
"""

    def _integration_template(self) -> str:
        return """# {function_name}

## 1. Feature Overview
{user_input}

## 2. Integration Requirements
- [ ] Connect to third-party service
- [ ] Handle authentication
- [ ] Process responses
- [ ] Handle errors gracefully

## 3. Integration Details
- **Provider**: [Third-party name]
- **Authentication**: [Auth method]
- **Endpoints**: [API endpoints]

## 4. Error Handling
- [ ] Network errors handled
- [ ] API errors reported
- [ ] Retry logic implemented

## 5. Acceptance Criteria
- [ ] Integration works in happy path
- [ ] Errors are handled properly
- [ ] Data is processed correctly
"""

    def _ui_template(self) -> str:
        return """# {function_name}

## 1. Feature Overview
{user_input}

## 2. User Story
As a {target_users}, I want to {features}, so that {value_proposition}.

## 3. Functional Requirements
- [ ] UI renders correctly
- [ ] User interactions work
- [ ] Data displays properly

## 4. UI Components
- [ ] Main component
- [ ] Supporting components

## 5. Acceptance Criteria
- [ ] UI renders without errors
- [ ] User can interact with elements
- [ ] Responsive on different screens
"""

    def _script_template(self) -> str:
        return """# {function_name}

## 1. Feature Overview
{user_input}

## 2. Functional Requirements
- [ ] Script runs without errors
- [ ] Accepts required parameters
- [ ] Produces expected output

## 3. Usage
```bash
helix {domain} --help
```

## 4. Acceptance Criteria
- [ ] Script executes successfully
- [ ] Output is correct
- [ ] Error handling works
"""

    def _infrastructure_template(self) -> str:
        return """# {function_name}

## 1. Feature Overview
{user_input}

## 2. Functional Requirements
- [ ] Deployment configuration complete
- [ ] CI/CD pipeline works
- [ ] Infrastructure is reproducible

## 3. Configuration
- [ ] Environment variables defined
- [ ] Secrets managed properly
- [ ] Resources provisioned

## 4. Acceptance Criteria
- [ ] Deploys successfully
- [ ] CI/CD runs without errors
- [ ] Infrastructure is stable
"""

    def _general_template(self) -> str:
        return """# {function_name}

## 1. Feature Overview
{user_input}

## 2. User Story
As a {target_users}, I want to {features}, so that {value_proposition}.

## 3. Functional Requirements
- [ ] Core functionality implemented
- [ ] Edge cases handled
- [ ] User experience is good

## 4. Acceptance Criteria
- [ ] Feature works as expected
- [ ] No critical bugs
- [ ] Performance is acceptable
"""
