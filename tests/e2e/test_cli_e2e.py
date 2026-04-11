"""
End-to-End tests for Helix CLI

These tests verify the core CLI workflows work correctly.
"""

import pytest
import subprocess
from pathlib import Path


# Use the installed helix command
HELIX_CMD = "helix"


class TestCLIHelp:
    """Test CLI help commands"""

    def test_helix_help(self):
        """Test helix --help works"""
        result = subprocess.run(
            [HELIX_CMD, "--help"],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0
        assert "Helix" in result.stdout

    def test_helix_list_skills(self):
        """Test helix list-skills works"""
        result = subprocess.run(
            [HELIX_CMD, "list-skills"],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0
        assert "spec" in result.stdout
        assert "build" in result.stdout

    def test_helix_status(self):
        """Test helix status works"""
        result = subprocess.run(
            [HELIX_CMD, "status"],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0
        assert "Helix" in result.stdout
        assert "RC" in result.stdout


class TestCLIVersion:
    """Test CLI version"""

    def test_version_output(self):
        """Test version is correctly displayed"""
        result = subprocess.run(
            [HELIX_CMD, "status"],
            capture_output=True,
            text=True,
        )
        assert "1.0.0-rc.1" in result.stdout


class TestSkillCommands:
    """Test individual skill commands"""

    def test_spec_help(self):
        """Test helix spec --help"""
        result = subprocess.run(
            [HELIX_CMD, "spec", "--help"],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0

    def test_build_help(self):
        """Test helix build --help"""
        result = subprocess.run(
            [HELIX_CMD, "build", "--help"],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0

    def test_verify_help(self):
        """Test helix verify --help"""
        result = subprocess.run(
            [HELIX_CMD, "verify", "--help"],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0

    def test_ship_help(self):
        """Test helix ship --help"""
        result = subprocess.run(
            [HELIX_CMD, "ship", "--help"],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0
