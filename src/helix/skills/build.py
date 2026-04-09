"""
/build 技能 - 代码骨架生成

根据规格说明书生成代码骨架
"""

import asyncio
from dataclasses import dataclass, field
from typing import List, Optional
from pathlib import Path

from helix.skills.base import Skill, SkillResult, SkillConfig, SkillCategory, SkillStatus
from helix.core.intent import Intent, IntentType
from helix.core.context import HelixContext


# ============ 数据模型 ============

@dataclass
class FieldDef:
    """字段定义"""
    name: str
    field_type: str
    required: bool = True
    description: str = ""


@dataclass
class APIEndpoint:
    """API 端点"""
    method: str
    path: str
    description: str = ""


@dataclass
class TestCase:
    """测试用例"""
    name: str
    description: str = ""
    steps: List[str] = field(default_factory=list)
    expected: str = ""


@dataclass
class SpecDocument:
    """解析后的规格文档"""
    title: str = ""
    project: str = ""
    overview: str = ""
    features: List[str] = field(default_factory=list)
    apis: List[APIEndpoint] = field(default_factory=list)
    models: List[FieldDef] = field(default_factory=list)
    test_cases: List[TestCase] = field(default_factory=list)


@dataclass
class CodeFile:
    """生成的代码文件"""
    path: str
    content: str
    language: str = "python"


# ============ SpecParser ============

class SpecParser:
    """规格说明书解析器"""

    def parse(self, spec_content: str) -> SpecDocument:
        """解析 Markdown 规格文件"""
        doc = SpecDocument()

        lines = spec_content.split('\n')
        in_section = None
        section_content = []

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
    """代码生成器"""

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

        model_content = f'''"""数据模型"""
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
        api_content = f'''"""API 路由"""
from fastapi import APIRouter, HTTPException
from typing import List
from models.{domain} import {model_name}, {model_name}Create, {model_name}Update

router = APIRouter(prefix="/api/{domain}", tags=["{domain}"])

@router.get("", response_model=List[{model_name}])
async def list_{domain}():
    """获取{domain}列表"""
    # TODO: 实现列表查询
    return []

@router.get("/{{item_id}}", response_model={model_name})
async def get_{domain}(item_id: str):
    """获取单个{domain}"""
    # TODO: 实现查询
    raise HTTPException(status_code=404)

@router.post("", response_model={model_name})
async def create_{domain}(item: {model_name}Create):
    """创建{domain}"""
    # TODO: 实现创建
    pass

@router.put("/{{item_id}}", response_model={model_name})
async def update_{domain}(item_id: str, item: {model_name}Update):
    """更新{domain}"""
    # TODO: 实现更新
    raise HTTPException(status_code=404)

@router.delete("/{{item_id}}")
async def delete_{domain}(item_id: str):
    """删除{domain}"""
    # TODO: 实现删除
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
        test_content = f'''"""测试用例"""
import pytest
from fastapi.testclient import TestClient

def test_list_{domain}(client: TestClient):
    """测试获取{domain}列表"""
    response = client.get("/api/{domain}")
    assert response.status_code == 200

def test_create_{domain}(client: TestClient):
    """测试创建{domain}"""
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
        main_content = f'''"""FastAPI 应用入口"""
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


# ============ BuildSkill ============

class BuildSkill(Skill):
    """代码骨架生成技能"""

    name = "build"
    description = "根据规格说明书生成代码骨架"
    category = SkillCategory.EXECUTION
    status = SkillStatus.DRAFT

    examples = [
        "helix build SPEC.md",
        "helix build SPEC.md --framework fastapi",
    ]

    async def execute(self, intent: Intent, context: HelixContext) -> SkillResult:
        self.initialize()
        start_time = asyncio.get_event_loop().time()

        spec_file = intent.parameters.get('spec_file', '')
        framework = intent.parameters.get('framework', 'fastapi')
        output_dir = intent.parameters.get('output', '.')

        if not spec_file:
            return SkillResult(
                success=False,
                message="请指定规格说明书文件",
                skill_name=self.name
            )

        spec_path = Path(spec_file)
        if not spec_path.exists():
            return SkillResult(
                success=False,
                message=f"文件不存在: {spec_file}",
                skill_name=self.name
            )

        spec_content = spec_path.read_text()
        parser = SpecParser()
        spec = parser.parse(spec_content)

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
            message=f"已生成 {len(files)} 个文件",
            data={
                "spec_title": spec.title,
                "framework": framework,
                "files": generated_files,
            },
            skill_name=self.name,
            execution_time_ms=execution_time,
        )
