"""Test Build Skill"""

import pytest
from helix.skills.build import (
    BuildSkill,
    SpecParser,
    CodeGenerator,
    FieldDef,
    APIEndpoint,
    TestCase,
    SpecDocument,
    CodeFile,
)
from helix.skills.base import SkillConfig


class TestBuildSkill:
    """Test BuildSkill"""

    @pytest.fixture
    def skill(self):
        return BuildSkill()

    def test_skill_init(self, skill):
        """Test skill initialization"""
        assert skill.name == "build"

    def test_skill_examples(self, skill):
        """Test skill examples"""
        assert len(skill.examples) > 0


class TestFieldDef:
    """Test FieldDef dataclass"""

    def test_field_def_creation(self):
        """Test creating a field definition"""
        field = FieldDef(name="username", field_type="str", required=True, description="User name")
        assert field.name == "username"
        assert field.field_type == "str"
        assert field.required is True


class TestAPIEndpoint:
    """Test APIEndpoint dataclass"""

    def test_api_endpoint_creation(self):
        """Test creating an API endpoint"""
        endpoint = APIEndpoint(method="GET", path="/users", description="Get all users")
        assert endpoint.method == "GET"
        assert endpoint.path == "/users"


class TestTestCase:
    """Test TestCase dataclass"""

    def test_test_case_creation(self):
        """Test creating a test case"""
        test_case = TestCase(name="test_login", description="Test login", steps=["enter username", "enter password"], expected="logged in")
        assert test_case.name == "test_login"
        assert len(test_case.steps) == 2


class TestSpecDocument:
    """Test SpecDocument dataclass"""

    def test_spec_document_creation(self):
        """Test creating a spec document"""
        doc = SpecDocument(
            title="Test Project",
            project="test",
            overview="Overview",
            features=["feature1"],
            apis=[APIEndpoint("GET", "/test")],
            models=[FieldDef("id", "int")],
            test_cases=[TestCase("test1")]
        )
        assert doc.title == "Test Project"
        assert len(doc.features) == 1
        assert len(doc.apis) == 1
        assert len(doc.models) == 1
        assert len(doc.test_cases) == 1


class TestCodeFile:
    """Test CodeFile dataclass"""

    def test_code_file_creation(self):
        """Test creating a code file"""
        code_file = CodeFile(path="main.py", content="print('hello')", language="python")
        assert code_file.path == "main.py"
        assert code_file.content == "print('hello')"
        assert code_file.language == "python"


class TestSpecParser:
    """Test SpecParser class"""

    def test_spec_parser_init(self):
        """Test spec parser initialization"""
        parser = SpecParser()
        assert parser is not None

    def test_parse_simple_spec(self):
        """Test parsing a simple specification"""
        parser = SpecParser()
        spec = """# Test Project

## Overview
This is a test project.
"""
        doc = parser.parse(spec)
        assert doc is not None
        assert doc.title == "Test Project"


class TestCodeGenerator:
    """Test CodeGenerator class"""

    def test_code_generator_init(self):
        """Test code generator initialization"""
        generator = CodeGenerator(framework="fastapi")
        assert generator.framework == "fastapi"

    def test_code_generator_default_framework(self):
        """Test default framework"""
        generator = CodeGenerator()
        assert generator.framework == "fastapi"