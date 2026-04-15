"""Tests for docs generator module"""

import pytest
from helix.docs.generator import (
    generate_readme,
    generate_architecture_doc,
    generate_changelog,
    run_docs_generator,
)
from pathlib import Path
import tempfile


class TestGenerateReadme:
    """Test README generation"""

    def test_generate_readme_default(self):
        """Test default README generation"""
        result = generate_readme()
        assert "# Helix" in result
        assert "AI Era Software Engineering Methodology" in result
        assert "## Quick Start" in result
        assert "## Skills" in result

    def test_generate_readme_custom(self):
        """Test custom README generation"""
        result = generate_readme(project_name="TestProject", description="Test description")
        assert "# TestProject" in result
        assert "Test description" in result


class TestGenerateArchitectureDoc:
    """Test architecture documentation generation"""

    def test_generate_architecture_doc(self):
        """Test architecture doc generation"""
        result = generate_architecture_doc()
        assert "# Helix Architecture" in result
        assert "## Design Principles" in result
        assert "## Four-Layer Architecture" in result
        assert "L4: Meta-Methodology" in result
        assert "L3: Execution Engine" in result


class TestGenerateChangelog:
    """Test changelog generation"""

    def test_generate_changelog_empty(self):
        """Test changelog with no existing content"""
        result = generate_changelog()
        assert "# Changelog" in result
        assert "v0.9.0" in result
        assert "Production Ready" in result

    def test_generate_changelog_existing(self):
        """Test changelog with existing content"""
        existing = "# Changelog\n\n## v0.8.0\nOld content"
        result = generate_changelog(existing)
        assert "# Changelog" in result


class TestRunDocsGenerator:
    """Test docs generator runner"""

    def test_run_docs_generator(self):
        """Test running docs generator"""
        with tempfile.TemporaryDirectory() as tmpdir:
            run_docs_generator(tmpdir)

            readme_path = Path(tmpdir) / "README.md"
            arch_path = Path(tmpdir) / "ARCHITECTURE.md"
            changelog_path = Path(tmpdir) / "CHANGELOG.md"

            assert readme_path.exists()
            assert arch_path.exists()
            assert changelog_path.exists()

            assert readme_path.read_text().startswith("# Helix")
            assert arch_path.read_text().startswith("# Helix Architecture")
            assert changelog_path.read_text().startswith("# Changelog")