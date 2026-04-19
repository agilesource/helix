"""
/build Skill - Code Scaffolding Generation

Generate code scaffolding from specifications.
"""

import asyncio
import re
from dataclasses import dataclass, field
from typing import List, Optional
from pathlib import Path

from helix.skills.base import Skill, SkillResult, SkillConfig, SkillCategory, SkillStatus
from helix.core.intent import Intent, IntentType
from helix.core.context import HelixContext
from helix.adapters.llm import get_llm_adapter, AIRequest
from rich.console import Console


# ============ LLM Code Generation Prompts ============

LLM_CODE_SYSTEM_PROMPT = """You are an expert software engineer. Generate high-quality, production-ready code based on specifications.
Your code should:
1. Follow best practices and patterns
2. Include proper error handling
3. Have meaningful variable/function names
4. Include docstrings and comments
5. Be secure (no SQL injection, proper input validation)
6. Handle edge cases

Output ONLY the code, no explanations."""


LLM_CODE_GENERATION_PROMPT = """Generate a complete {framework} application based on this specification:

{spec}

Requirements:
- Use {framework} framework
- Include proper models, routes, and business logic
- Add input validation
- Include error handling
- Add docstrings

Generate these files:
1. models.py - Data models with Pydantic validation
2. routes.py - API routes with proper HTTP methods
3. main.py - Application entry point
4. requirements.txt - Dependencies

Output each file with format:
```filename: <filename>
<code here>
```

Start each file with this marker."""


# ============ Data Models ============

@dataclass
class FieldDef:
    """Field definition"""
    name: str
    field_type: str
    required: bool = True
    description: str = ""


@dataclass
class APIEndpoint:
    """API endpoint"""
    method: str
    path: str
    description: str = ""


@dataclass
class TestCase:
    """Test case"""
    name: str
    description: str = ""
    steps: List[str] = field(default_factory=list)
    expected: str = ""


@dataclass
class SpecDocument:
    """Parsed specification document"""
    title: str = ""
    project: str = ""
    overview: str = ""
    features: List[str] = field(default_factory=list)
    apis: List[APIEndpoint] = field(default_factory=list)
    models: List[FieldDef] = field(default_factory=list)
    test_cases: List[TestCase] = field(default_factory=list)


@dataclass
class CodeFile:
    """Generated code file"""
    path: str
    content: str
    language: str = "python"


# ============ SpecParser ============

class SpecParser:
    """Specification parser"""

    def parse(self, spec_content: str) -> SpecDocument:
        """Parse Markdown specification file"""
        doc = SpecDocument()

        lines = spec_content.split('\n')
        in_section = None
        section_content: list[str] = []

        for line in lines:
            if line.startswith('## '):
                self._process_section(doc, in_section, section_content)
                in_section = line.replace('## ', '').strip()
                section_content = []
            elif line.startswith('# '):
                doc.title = line.replace('# ', '').strip()
            elif line.startswith('> '):
                doc.project = line.replace('> 项目: ', '').strip()
            else:
                section_content.append(line)

        self._process_section(doc, in_section, section_content)
        return doc

    def _process_section(self, doc: SpecDocument, section: Optional[str], content: List[str]):
        if not section:
            return

        section_text = '\n'.join(content)

        if '功能概述' in section:
            doc.overview = section_text.strip()
        elif '功能需求' in section:
            for line in content:
                if '|' in line and '功能点' not in line and '---' not in line:
                    parts = [p.strip() for p in line.split('|')]
                    if len(parts) >= 3 and parts[1]:
                        doc.features.append(parts[1])
        elif '接口设计' in section:
            self._parse_apis(doc, content)
        elif '数据模型' in section:
            self._parse_models(doc, content)
        elif '验收标准' in section:
            self._parse_tests(doc, content)

    def _parse_apis(self, doc: SpecDocument, content: List[str]):
        for line in content:
            if '|' in line and '方法' not in line and '---' not in line:
                parts = [p.strip() for p in line.split('|')]
                if len(parts) >= 3 and parts[1]:
                    method = parts[1].upper()
                    path = parts[2]
                    desc = parts[3] if len(parts) > 3 else ""
                    doc.apis.append(APIEndpoint(method=method, path=path, description=desc))

    def _parse_models(self, doc: SpecDocument, content: List[str]):
        for line in content:
            if '|' in line and '字段' not in line and '---' not in line:
                parts = [p.strip() for p in line.split('|')]
                if len(parts) >= 4 and parts[1]:
                    name = parts[1]
                    field_type = parts[2]
                    required = '是' in parts[3]
                    desc = parts[4] if len(parts) > 4 else ""
                    doc.models.append(FieldDef(name=name, field_type=field_type,
                                               required=required, description=desc))

    def _parse_tests(self, doc: SpecDocument, content: List[str]):
        for line in content:
            if '- [ ]' in line:
                test_name = line.replace('- [ ]', '').strip()
                doc.test_cases.append(TestCase(name=test_name))


# ============ CodeGenerator ============

class CodeGenerator:
    """Code generator"""

    def __init__(self, framework: str = "fastapi"):
        self.framework = framework

    def generate(self, spec: SpecDocument) -> List[CodeFile]:
        files = []
        if self.framework == "fastapi":
            files.extend(self._generate_fastapi(spec))
        return files

    def _generate_fastapi(self, spec: SpecDocument) -> List[CodeFile]:
        files = []
        domain = self._infer_domain(spec)
        model_name = self._to_class_name(domain)

        # 1. models/__init__.py
        files.append(CodeFile(
            path="models/__init__.py",
            content=f"from .{domain} import {model_name}\n\nexport = ['{model_name}']\n"
        ))

        # 2. models/{domain}.py
        model_fields = "\n    ".join([
            f"{m.name}: {self._py_type(m.field_type)}{'' if m.required else ' = None'}"
            for m in spec.models
        ]) or "id: str"

        model_content = f'''"""Data models"""
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class {model_name}Base(BaseModel):
    {model_fields}

class {model_name}({model_name}Base):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class {model_name}Create({model_name}Base):
    pass

class {model_name}Update(BaseModel):
    pass
'''
        files.append(CodeFile(path=f"models/{domain}.py", content=model_content))

        # 3. api/__init__.py
        files.append(CodeFile(
            path="api/__init__.py",
            content=f"from api.{domain} import router\n\n__all__ = ['router']\n"
        ))

        # 4. api/{domain}.py
        api_content = f'''"""API routes"""
from fastapi import APIRouter, HTTPException
from typing import List
from models.{domain} import {model_name}, {model_name}Create, {model_name}Update

router = APIRouter(prefix="/api/{domain}", tags=["{domain}"])

@router.get("", response_model=List[{model_name}])
async def list_{domain}():
    """List {domain}"""
    # TODO: implement list query
    return []

@router.get("/{{item_id}}", response_model={model_name})
async def get_{domain}(item_id: str):
    """Get single {domain}"""
    # TODO: implement get
    raise HTTPException(status_code=404)

@router.post("", response_model={model_name})
async def create_{domain}(item: {model_name}Create):
    """Create {domain}"""
    # TODO: implement create
    pass

@router.put("/{{item_id}}", response_model={model_name})
async def update_{domain}(item_id: str, item: {model_name}Update):
    """Update {domain}"""
    # TODO: implement update
    raise HTTPException(status_code=404)

@router.delete("/{{item_id}}")
async def delete_{domain}(item_id: str):
    """Delete {domain}"""
    # TODO: implement delete
    return {{"status": "deleted"}}
'''
        files.append(CodeFile(path=f"api/{domain}.py", content=api_content))

        # 5. tests/__init__.py
        files.append(CodeFile(path="tests/__init__.py", content=""))

        # 5.1 tests/conftest.py - pytest fixtures
        conftest_content = '''"""Pytest fixtures"""
import pytest
from fastapi.testclient import TestClient
from main import app

@pytest.fixture
def client():
    """Test client fixture"""
    return TestClient(app)
'''
        files.append(CodeFile(path="tests/conftest.py", content=conftest_content))

        # 6. tests/test_{domain}.py
        test_content = f'''"""Test cases"""
import pytest
from fastapi.testclient import TestClient

def test_list_{domain}(client: TestClient):
    """Test list {domain}"""
    response = client.get("/api/{domain}")
    assert response.status_code == 200

def test_create_{domain}(client: TestClient):
    """Test create {domain}"""
    data = {{}}
    response = client.post("/api/{domain}", json=data)
    assert response.status_code in [200, 201]
'''
        files.append(CodeFile(path=f"tests/test_{domain}.py", content=test_content))

        # 7. requirements.txt
        files.append(CodeFile(
            path="requirements.txt",
            content="fastapi>=0.100.0\nuvicorn>=0.23.0\npydantic>=2.0.0\npytest>=7.4.0\nhttpx>=0.24.0\n"
        ))

        # 8. main.py
        main_content = f'''"""FastAPI application entry point"""
from fastapi import FastAPI
from api import router

app = FastAPI(
    title="{spec.title or domain}",
    description="{spec.overview or ''}",
    version="0.1.0"
)

app.include_router(router)

@app.get("/health")
def health_check():
    return {{"status": "healthy"}}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
'''
        files.append(CodeFile(path="main.py", content=main_content))

        return files

    def _infer_domain(self, spec: SpecDocument) -> str:
        title = spec.title.lower()
        if '用户' in title or 'user' in title:
            return 'users'
        if '订单' in title or 'order' in title:
            return 'orders'
        if '商品' in title or 'product' in title:
            return 'products'
        for f in spec.features:
            if '用户' in f or 'user' in f.lower():
                return 'users'
        return 'items'

    def _to_class_name(self, name: str) -> str:
        return ''.join(word.capitalize() for word in name.split('_'))

    def _py_type(self, field_type: str) -> str:
        type_map = {
            'string': 'str', 'int': 'int', 'integer': 'int',
            'float': 'float', 'bool': 'bool', 'boolean': 'bool',
            'datetime': 'datetime', 'uuid': 'str',
        }
        return type_map.get(field_type.lower(), 'str')


# ============ LLM Code Generator ============

class LLMCodeGenerator:
    """LLM-enhanced code generator"""

    def __init__(self, framework: str = "fastapi"):
        self.framework = framework
        self._llm_adapter = None

    def _get_llm_adapter(self):
        """Get LLM adapter (lazy load)"""
        if self._llm_adapter is None:
            self._llm_adapter = get_llm_adapter()
        return self._llm_adapter

    async def generate(self, spec_content: str) -> Optional[List[CodeFile]]:
        """Generate code using LLM"""
        adapter = self._get_llm_adapter()

        if not adapter or not adapter.is_available():
            # Fallback to template generator
            return None

        prompt = LLM_CODE_GENERATION_PROMPT.format(
            framework=self.framework,
            spec=spec_content
        )

        response = await adapter.execute(
            AIRequest(
                prompt=prompt,
                context=LLM_CODE_SYSTEM_PROMPT
            )
        )

        if not response.success:
            return None

        return self._parse_llm_output(response.content)

    def _parse_llm_output(self, content: str) -> List[CodeFile]:
        """Parse LLM output into code files"""
        files = []
        current_filename = None
        current_content: list[str] = []

        for line in content.split('\n'):
            # Check for file marker
            if '```filename:' in line.lower():
                # Save previous file
                if current_filename and current_content:
                    files.append(CodeFile(
                        path=current_filename,
                        content='\n'.join(current_content)
                    ))

                # Extract filename
                match = re.search(r'filename:\s*(\S+)', line, re.IGNORECASE)
                if match:
                    current_filename = match.group(1)
                    current_content = []
                continue

            # Check for code block end
            if line.strip() == '```' and current_filename:
                continue

            # Add content to current file
            if current_filename:
                current_content.append(line)

        # Save last file
        if current_filename and current_content:
            files.append(CodeFile(
                path=current_filename,
                content='\n'.join(current_content)
            ))

        return files


# ============ BuildSkill ============

class BuildSkill(Skill):
    """Code scaffolding generation skill"""

    name = "build"
    description = "Generate code scaffolding from specification"
    category = SkillCategory.EXECUTION
    status = SkillStatus.DRAFT

    examples = [
        "helix build SPEC.md",
        "helix build SPEC.md --framework fastapi",
        "helix build 'user login feature'",
    ]

    def __init__(self, config: Optional[SkillConfig] = None):
        super().__init__(config)
        self.console = Console()
        self._spec_skill = None

    def _do_initialize(self) -> None:
        """Initialize skills"""
        # Import here to avoid circular dependency
        from helix.skills.spec import SpecSkill

        self._spec_skill = SpecSkill()

    async def execute(self, intent: Intent, context: HelixContext) -> SkillResult:
        self.initialize()
        start_time = asyncio.get_event_loop().time()

        # Check if input is a spec file or requirement text
        spec_file = intent.parameters.get('spec_file', '')
        requirement_text = intent.parameters.get('requirement', '')
        framework = intent.parameters.get('framework', 'fastapi')
        output_dir = intent.parameters.get('output', '.')
        use_llm = intent.parameters.get('use_llm', False)

        # If requirement text provided, generate spec first
        spec_content = None
        if requirement_text and not spec_file:
            self.console.print("[dim]Generating specification...[/dim]")
            spec_intent = Intent(
                type=IntentType.SPEC,
                raw_input=requirement_text,
                confidence=0.9,
                parameters={}
            )
            spec_result = await self._spec_skill.execute(spec_intent, context)  # type: ignore[attr-defined]
            if spec_result.success:
                spec_content = spec_result.artifacts.get('spec', '') if spec_result.artifacts else spec_result.data.get('spec_content', '')
                self.console.print("[dim]Specification generated.[/dim]\n")
            else:
                return SkillResult(
                    success=False,
                    message=f"Spec generation failed: {spec_result.message}",
                    skill_name=self.name
                )

        # Parse spec from file or generated content
        if spec_file:
            spec_path = Path(spec_file)
            if not spec_path.exists():
                return SkillResult(
                    success=False,
                    message=f"File not found: {spec_file}",
                    skill_name=self.name
                )
            spec_content = spec_path.read_text()
        elif not spec_content:
            return SkillResult(
                success=False,
                message="Please provide spec file or requirement text",
                skill_name=self.name
            )

        # Parse and generate code
        parser = SpecParser()
        spec = parser.parse(spec_content)

        files = []
        llm_used = False

        # Try LLM generation if requested
        if use_llm:
            self.console.print("[dim]Generating code with LLM...[/dim]")
            llm_generator = LLMCodeGenerator(framework=framework)
            llm_files = await llm_generator.generate(spec_content)
            if llm_files:
                files = llm_files
                llm_used = True
                self.console.print("[dim]LLM code generation complete.[/dim]\n")
            else:
                self.console.print("[dim]LLM unavailable, using template...[/dim]\n")

        # Fallback to template generator
        if not files:
            generator = CodeGenerator(framework=framework)
            files = generator.generate(spec)

        output_path = Path(output_dir)
        generated_files = []

        for code_file in files:
            file_path = output_path / code_file.path
            file_path.parent.mkdir(parents=True, exist_ok=True)
            file_path.write_text(code_file.content)
            generated_files.append(code_file.path)

        execution_time = int((asyncio.get_event_loop().time() - start_time) * 1000)

        return SkillResult(
            success=True,
            message=f"Generated {len(files)} files {'(LLM)' if llm_used else ''}",
            data={
                "spec_title": spec.title,
                "framework": framework,
                "files": generated_files,
                "requirement": requirement_text or spec_file,
                "llm_used": llm_used,
            },
            skill_name=self.name,
            execution_time_ms=execution_time,
        )
