"""
/spec 技能 - 规格说明书生成

将用户需求转化为结构化规格说明书
"""

import asyncio
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from enum import Enum
import re

from helix.skills.base import Skill, SkillResult, SkillConfig, SkillCategory, SkillStatus
from helix.core.intent import Intent, IntentType
from helix.core.context import HelixContext


class RequirementType(Enum):
    """需求类型"""

    CRUD = "crud"           # 创建/读取/更新/删除
    API = "api"             # API 服务
    ALGORITHM = "algorithm" # 算法实现
    INTEGRATION = "integration" # 第三方集成
    UI = "ui"               # 页面/组件
    SCRIPT = "script"       # 脚本工具
    INFRASTRUCTURE = "infrastructure" # 基础设施
    GENERAL = "general"     # 通用需求


@dataclass
class ExtractedEntities:
    """从需求中提取的实体"""

    domain: str = ""          # 领域：用户、订单、支付
    action: str = ""          # 动作：登录、查询、创建
    entities: List[str] = field(default_factory=list)  # 涉及的实体
    integrations: List[str] = field(default_factory=list)  # 第三方集成
    constraints: List[str] = field(default_factory=list)  # 约束条件
    target_users: List[str] = field(default_factory=list)  # 目标用户
    value_proposition: str = ""  # 用户价值
    features: List[str] = field(default_factory=list)  # 具体功能点
    project_context: str = ""  # 项目背景


@dataclass
class SpecSection:
    """规格说明书章节"""

    title: str
    content: str
    required: bool = True


class SpecSkill(Skill):
    """规格说明书生成技能"""

    name = "spec"
    description = "将用户需求转化为结构化规格说明书"
    category = SkillCategory.EXECUTION
    status = SkillStatus.DRAFT

    examples = [
        "我想做一个用户登录功能",
        "创建一个用户管理 API",
        "实现一个推荐算法",
    ]

    # 模板目录
    TEMPLATE_DIR = ".helix/templates/spec"

    def __init__(self, config: Optional[SkillConfig] = None):
        super().__init__(config)
        self._templates: Dict[RequirementType, str] = {}
        self._socratic_questions: List[Dict[str, str]] = []

    def _do_initialize(self) -> None:
        """加载模板"""
        self._load_templates()
        self._load_socratic_questions()

    def _load_templates(self) -> None:
        """加载规格说明书模板"""
        # 基础模板结构 - 实际使用时由 AI 填充
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

    def _load_socratic_questions(self) -> None:
        """加载 Socratic 提问模板"""
        self._socratic_questions = [
            {"key": "domain", "question": "请问这个功能属于什么业务领域？", "when": "domain_missing"},
            {"key": "target_user", "question": "请描述一下目标用户是谁？", "when": "target_user_missing"},
            {"key": "value", "question": "这个功能为用户解决什么问题？", "when": "value_missing"},
            {"key": "scale", "question": "预计有多少用户会使用这个功能？", "when": "scale_missing"},
            {"key": "integration", "question": "需要与哪些第三方系统对接？", "when": "integration_missing"},
            {"key": "platform", "question": "需要支持哪些平台（Web/iOS/Android）？", "when": "platform_missing"},
            {"key": "acceptance", "question": "你如何判断这个功能做完了？", "when": "acceptance_missing"},
        ]

    async def execute(self, intent: Intent, context: HelixContext) -> SkillResult:
        """执行技能"""
        self.initialize()
        start_time = asyncio.get_event_loop().time()

        user_input = intent.raw_input

        # Step 1: 意图解析 - 识别需求类型
        req_type = self._classify_requirement(user_input)
        entities = self._extract_entities(user_input)

        # Step 2: 需求澄清 - Socratic 提问
        clarifications = await self._clarify_requirements(user_input, entities, context)

        # Step 3: 模板选择与规格生成
        spec_content = self._generate_spec(user_input, req_type, entities, clarifications)

        # Step 4: 人类确认 (这里先返回，让 CLI 层处理)
        execution_time = int((asyncio.get_event_loop().time() - start_time) * 1000)

        return SkillResult(
            success=True,
            message="规格说明书已生成",
            data={
                "requirement_type": req_type.value,
                "entities": {
                    "domain": entities.domain,
                    "action": entities.action,
                    "entities": entities.entities,
                },
                "clarifications": clarifications,
                "spec_content": spec_content,
            },
            skill_name=self.name,
            execution_time_ms=execution_time,
            artifacts={"spec": spec_content},
        )

    def _classify_requirement(self, user_input: str) -> RequirementType:
        """识别需求类型"""
        input_lower = user_input.lower()

        # 关键词匹配 - 按优先级排序
        # 登录/认证 优先识别为 CRUD (后端)
        if any(kw in input_lower for kw in ["登录", "注册", "认证", "验证", "登出", "找回密码", "oauth"]):
            return RequirementType.CRUD

        if any(kw in input_lower for kw in ["创建", "添加", "删除", "修改", "管理", "crud"]):
            return RequirementType.CRUD

        if any(kw in input_lower for kw in ["api", "接口", "服务", "rest", "graphql"]):
            return RequirementType.API
        if any(kw in input_lower for kw in ["算法", "计算", "排序", "搜索", "推荐"]):
            return RequirementType.ALGORITHM
        if any(kw in input_lower for kw in ["集成", "对接", "第三方", "stripe", "支付"]):
            return RequirementType.INTEGRATION
        if any(kw in input_lower for kw in ["页面", "组件", "ui", "前端", "登录", "表单"]):
            return RequirementType.UI
        if any(kw in input_lower for kw in ["脚本", "工具", "命令行", "cli"]):
            return RequirementType.SCRIPT
        if any(kw in input_lower for kw in ["部署", "ci", "cd", "配置", "docker", "k8s"]):
            return RequirementType.INFRASTRUCTURE

        return RequirementType.GENERAL

    def _extract_entities(self, user_input: str) -> ExtractedEntities:
        """提取实体 - 增强版"""
        entities = ExtractedEntities()

        # 提取领域 (简单的关键词匹配)
        domain_keywords = {
            "用户": ["用户", "登录", "注册", "认证", "权限", "角色"],
            "订单": ["订单", "购买", "支付", "结算"],
            "商品": ["商品", "产品", "库存", "SKU"],
            "内容": ["内容", "文章", "帖子", "评论"],
            "消息": ["消息", "通知", "推送", "邮件"],
            "文件": ["文件", "上传", "下载", "存储"],
        }

        for domain, keywords in domain_keywords.items():
            if any(kw in user_input for kw in keywords):
                entities.domain = domain
                break

        # 如果没找到明确领域，尝试从输入中提取
        if not entities.domain:
            # 尝试提取 "XX管理" 形式的领域
            import re
            match = re.search(r'(\w+)管理', user_input)
            if match:
                entities.domain = match.group(1)

        # 提取动作 - 多种动作用顿号分隔
        action_keywords = {
            "注册": ["注册", "signup", "创建账户"],
            "登录": ["登录", "登录", "认证", "验证", "login", "signin"],
            "权限": ["权限", "permission", "角色", "role", "授权"],
            "查询": ["查询", "获取", "列表", "搜索", "retrieve"],
            "创建": ["创建", "新增", "添加", "create"],
            "更新": ["更新", "修改", "编辑", "update"],
            "删除": ["删除", "移除", "delete"],
        }

        found_actions = []
        for action, keywords in action_keywords.items():
            if any(kw in user_input.lower() for kw in keywords):
                found_actions.append(action)

        if found_actions:
            entities.action = "、".join(found_actions)
            entities.features = found_actions

        # 提取目标用户 - 推断
        if "项目" in user_input or "Helix" in user_input:
            entities.target_users = ["开发者", "Helix 用户"]
        else:
            entities.target_users = ["最终用户"]

        # 提取价值 - 推断
        if "权限" in user_input or "角色" in user_input:
            entities.value_proposition = "实现细粒度的访问控制，保证系统安全"
        elif "登录" in user_input or "注册" in user_input:
            entities.value_proposition = "保护用户账户安全，提供便捷的认证体验"

        # 提取第三方集成
        integration_keywords = ["stripe", "paypal", "微信", "支付宝", "aws", "s3", "sendgrid", "twilio", "github", "google"]
        for kw in integration_keywords:
            if kw in user_input.lower():
                entities.integrations.append(kw)

        # 提取项目背景
        if "Helix" in user_input:
            entities.project_context = "Helix 项目"
        elif "项目" in user_input:
            import re
            match = re.search(r'为[^\s]+项目', user_input)
            if match:
                entities.project_context = match.group()

        return entities

    async def _clarify_requirements(
        self,
        user_input: str,
        entities: ExtractedEntities,
        context: HelixContext
    ) -> Dict[str, str]:
        """Socratic 提问 - 需求澄清"""
        clarifications = {}

        # 检查缺失信息
        missing = []
        if not entities.domain:
            missing.append("domain")
        if not entities.target_users:
            missing.append("target_user")
        if not entities.value_proposition:
            missing.append("value")
        if not entities.action:
            missing.append("action")

        # 最多提问 5 个问题
        max_questions = min(5, len(missing))

        # 在实际实现中，这里会启动交互式问答
        # 当前版本：返回缺失字段标记，由后续版本处理
        for key in missing[:max_questions]:
            clarifications[key] = f"[待澄清: {key}]"

        return clarifications

    def _generate_spec(
        self,
        user_input: str,
        req_type: RequirementType,
        entities: ExtractedEntities,
        clarifications: Dict[str, str]
    ) -> str:
        """生成规格说明书"""

        template = self._templates.get(req_type, self._templates[RequirementType.GENERAL])

        # 智能推断
        function_name = self._infer_function_name(user_input)
        domain = entities.domain or "未指定领域"
        action = entities.action or "未指定动作"

        # 使用提取的功能点
        features = entities.features if entities.features else [action]

        # 使用推断的目标用户
        target_users = ", ".join(entities.target_users) if entities.target_users else "最终用户"

        # 使用推断的价值
        value_prop = entities.value_proposition or "满足业务需求"

        # 使用项目背景
        project_ctx = entities.project_context or ""

        # 填充模板
        spec = template.format(
            function_name=function_name,
            domain=domain,
            action=action,
            features=", ".join(features),
            user_input=user_input,
            clarifications=self._format_clarifications(clarifications),
            target_users=target_users,
            value_proposition=value_prop,
            project_context=project_ctx,
        )

        return spec

    def _infer_function_name(self, user_input: str) -> str:
        """推断功能名称"""
        # 简单的名称提取
        import re
        # 去除常见前缀
        cleaned = re.sub(r"^(我想|我要|帮我|创建一个|做一个|实现一个)\s*", "", user_input)
        # 提取核心名词
        words = cleaned.split("的")
        if len(words) > 0:
            return words[-1].strip()
        return cleaned.strip()

    def _format_clarifications(self, clarifications: Dict[str, str]) -> str:
        """格式化澄清信息"""
        if not clarifications:
            return "无"
        lines = [f"- {k}: {v}" for k, v in clarifications.items()]
        return "\n".join(lines)

    # ============ 模板定义 ============

    def _crud_template(self) -> str:
        return """# {function_name}

> 项目: {project_context}

## 1. 功能概述
{user_input}

## 2. 用户故事
作为 [{target_users}]，我希望[{features}{domain}]，以便[{value_proposition}]。

## 3. 功能需求

### 3.1 核心功能 (P0)
| # | 功能点 | 验收标准 |
|---|--------|----------|
| 1 | {features} | 能成功执行操作并返回正确结果 |
| 2 | 数据验证 | 输入符合规则时成功，不符合时给出明确错误 |
| 3 | 权限控制 | 无权限用户无法执行操作 |

### 3.2 边缘功能 (P1)
| # | 功能点 | 验收标准 |
|---|--------|----------|
| 1 | 批量操作 | 支持批量处理 |
| 2 | 数据导出 | 支持导出为常见格式 |

## 4. 非功能需求
- **性能**: 单次操作响应时间 < 200ms
- **安全**: 敏感数据加密传输
- **兼容性**: 支持主流浏览器/客户端

## 5. 接口设计

### 5.1 API
| 方法 | 路径 | 描述 |
|------|------|------|
| GET | /api/{domain} | 获取{domain}列表 |
| GET | /api/{domain}/{{id}} | 获取单个{domain} |
| POST | /api/{domain} | 创建{domain} |
| PUT | /api/{domain}/{{id}} | 更新{domain} |
| DELETE | /api/{domain}/{{id}} | 删除{domain} |

### 5.2 数据模型
| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| id | UUID | 是 | 主键 |
| email | string | 是 | 邮箱地址 |
| password_hash | string | 是 | 密码哈希 |
| role | string | 是 | 角色(admin/user) |
| created_at | datetime | 是 | 创建时间 |
| updated_at | datetime | 是 | 更新时间 |

## 6. 验收标准 (AC)
- [ ] 正常情况下能完成{features}操作
- [ ] 异常输入给出清晰错误提示
- [ ] 无权限操作被正确拒绝
- [ ] 性能符合要求

## 7. 边界条件
- 空数据处理
- 并发冲突处理
- 网络异常处理

## 8. 技术约束
- 依赖: 需要用户认证模块
- 限制: 无

## 9. 风险与依赖
- 风险: 密码存储安全需符合 OWASP 标准
- 依赖: 用户表结构

{clarifications}
"""

    def _api_template(self) -> str:
        return """# {function_name}

## 1. 功能概述
{user_input}

## 2. 用户故事
作为 [API调用者]，我希望[调用{domain}相关API]，以便[实现业务功能]。

## 3. API 设计

### 3.1 接口列表
| 方法 | 路径 | 描述 |
|------|------|------|
| GET | /api/{domain} | 获取{domain}列表 |
| GET | /api/{domain}/{{id}} | 获取单个{domain} |
| POST | /api/{domain} | 创建{domain} |
| PUT | /api/{domain}/{{id}} | 更新{domain} |
| DELETE | /api/{domain}/{{id}} | 删除{domain} |

### 3.2 请求格式
```json
{{
  "field1": "value1",
  "field2": "value2"
}}
```

### 3.3 响应格式
```json
{{
  "success": true,
  "data": {{...}},
  "error": null
}}
```

## 4. 认证与授权
- 认证方式: Bearer Token
- 权限控制: 基于角色

## 5. 错误处理
| 状态码 | 含义 |
|--------|------|
| 400 | 请求参数错误 |
| 401 | 未认证 |
| 403 | 无权限 |
| 404 | 资源不存在 |
| 500 | 服务器错误 |

## 6. 验收标准 (AC)
- [ ] 接口返回正确格式
- [ ] 认证正常工作
- [ ] 错误情况正确处理
- [ ] 性能符合要求

## 7. 待澄清
{clarifications}
"""

    def _algorithm_template(self) -> str:
        return """# {function_name}

## 1. 功能概述
{user_input}

## 2. 算法描述
### 2.1 输入
- 参数1: 类型, 描述
- 参数2: 类型, 描述

### 2.2 输出
- 返回值: 类型, 描述

### 2.3 算法步骤
1. 步骤一
2. 步骤二
3. 步骤三

## 3. 复杂度分析
- 时间复杂度:
- 空间复杂度:

## 4. 边界条件
- 空输入
- 极大输入
- 特殊值

## 5. 测试用例
| 输入 | 预期输出 |
|------|----------|
| case1 | output1 |
| case2 | output2 |

## 6. 验收标准 (AC)
- [ ] 正确处理所有测试用例
- [ ] 性能满足要求
- [ ] 代码可读性良好

## 7. 待澄清
{clarifications}
"""

    def _integration_template(self) -> str:
        return """# {function_name}

## 1. 功能概述
{user_input}

## 2. 集成概述
### 2.1 第三方服务
- 服务名称:
- 用途:
- 文档链接:

### 2.2 集成方式
- API 调用
- Webhook
- SDK 集成

## 3. 功能需求

### 3.1 核心功能
| # | 功能点 | 验收标准 |
|---|--------|----------|
| 1 | 连接第三方服务 | 能成功建立连接 |
| 2 | 发送/接收数据 | 数据传输正确 |

### 3.2 错误处理
- 网络异常处理
- 认证失败处理
- 服务不可用处理

## 4. 安全考虑
- 凭证管理
- 数据加密
- 访问控制

## 5. 回退策略
- 主服务不可用时的处理

## 6. 验收标准 (AC)
- [ ] 能成功集成第三方服务
- [ ] 错误情况正确处理
- [ ] 安全措施到位

## 7. 待澄清
{clarifications}
"""

    def _ui_template(self) -> str:
        return """# {function_name}

## 1. 功能概述
{user_input}

## 2. 用户界面

### 2.1 页面结构
- 页面名称:
- 主要区域: 头部、内容区、底部

### 2.2 交互设计
| 元素 | 交互 | 反馈 |
|------|------|------|
| 按钮 | 点击 | 状态变化 |
| 表单 | 提交 | 验证反馈 |
| 列表 | 滚动 | 加载更多 |

### 2.3 状态定义
| 状态 | 描述 |
|------|------|
| 正常 | 默认状态 |
| 加载中 | 请求处理中 |
| 成功 | 操作完成 |
| 错误 | 异常状态 |
| 空数据 | 无内容显示 |

## 3. 响应式设计
- 桌面端: >= 1024px
- 平板端: 768px - 1023px
- 移动端: < 768px

## 4. 验收标准 (AC)
- [ ] 所有交互正常工作
- [ ] 响应式布局正确
- [ ] 无障碍支持
- [ ] 性能符合要求

## 5. 待澄清
{clarifications}
"""

    def _script_template(self) -> str:
        return """# {function_name}

## 1. 功能概述
{user_input}

## 2. 使用场景
- 场景1:
- 场景2:

## 3. 命令行接口

### 3.1 基本用法
```bash
helix-{function_name} [OPTIONS]
```

### 3.2 参数
| 参数 | 必填 | 描述 | 默认值 |
|------|------|------|--------|
| --input | 是 | 输入文件 | - |
| --output | 否 | 输出文件 | stdout |
| --config | 否 | 配置文件 | ./{function_name}.yaml |

### 3.3 输出格式
- JSON
- YAML
- 纯文本

## 4. 错误处理
| 错误码 | 含义 |
|--------|------|
| 1 | 参数错误 |
| 2 | 输入文件不存在 |
| 3 | 处理失败 |

## 5. 验收标准 (AC)
- [ ] 命令行参数正确解析
- [ ] 正确处理输入
- [ ] 错误情况给出清晰提示

## 6. 待澄清
{clarifications}
"""

    def _infrastructure_template(self) -> str:
        return """# {function_name}

## 1. 功能概述
{user_input}

## 2. 环境需求
- 操作系统:
- 依赖服务:
- 资源要求:

## 3. 配置

### 3.1 环境变量
| 变量名 | 必填 | 描述 |
|--------|------|------|
| ENV_VAR | 是 | 环境配置 |

### 3.2 配置文件
```yaml
# config.yaml
setting1: value1
setting2: value2
```

## 4. 部署步骤
1. 准备环境
2. 配置服务
3. 启动服务
4. 验证部署

## 5. 监控与告警
- 健康检查端点
- 关键指标
- 告警规则

## 6. 验收标准 (AC)
- [ ] 能正常部署
- [ ] 配置正确生效
- [ ] 监控告警工作正常

## 7. 待澄清
{clarifications}
"""

    def _general_template(self) -> str:
        return """# {function_name}

## 1. 功能概述
{user_input}

## 2. 详细描述
[请补充功能详细描述]

## 3. 功能需求
| # | 功能点 | 优先级 | 验收标准 |
|---|--------|--------|----------|
| 1 |        | P0    |          |

## 4. 非功能需求
- 性能:
- 安全:
- 可靠性:

## 5. 验收标准 (AC)
- [ ] 功能正常工作

## 6. 待澄清
{clarifications}
"""