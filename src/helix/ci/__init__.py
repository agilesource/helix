"""
Helix CI/CD Integration Helpers

GitHub Actions and other CI/CD system integration:
- Workflow generation
- Action triggers
- Status reporting
"""

import json
from pathlib import Path
from typing import Dict, Any, List, Optional
from dataclasses import dataclass


@dataclass
class CIWorkflow:
    """CI/CD workflow configuration"""
    name: str
    on: List[str]  # Triggers
    jobs: Dict[str, Any]


def generate_github_actions_workflow(
    project_type: str = "python",
    include_audit: bool = True,
    include_gate: bool = True,
) -> str:
    """Generate GitHub Actions workflow"""

    steps = [
        "uses: actions/checkout@v4",
        "uses: actions/setup-python@v5",
        "run: pip install -e .",
    ]

    if include_audit:
        steps.append("run: helix audit --security --dependencies")

    if include_gate:
        steps.append("run: helix gate --min-coverage 70")

    workflow = {
        "name": "Helix CI",
        "on": {
            "push": {"branches": ["main", "master"]},
            "pull_request": {"branches": ["main", "master"]},
        },
        "jobs": {
            "helix-ci": {
                "runs-on": "ubuntu-latest",
                "steps": steps,
            }
        }
    }

    return json.dumps(workflow, indent=2)


def generate_gitlab_ci_workflow(
    include_audit: bool = True,
    include_gate: bool = True,
) -> str:
    """Generate GitLab CI workflow"""

    stages = ["test", "audit", "deploy"]
    if include_gate:
        stages.insert(0, "gate")

    steps = [
        "pip install -e .",
    ]

    if include_audit:
        steps.append("helix audit --security --dependencies")

    if include_gate:
        steps.extend([
            "helix gate --min-coverage 70",
        ])

    workflow = {
        "stages": stages,
        "helix": {
            "stage": "gate",
            "script": steps,
            "only": ["main", "master"],
        }
    }

    return json.dumps(workflow, indent=2)


def create_github_actions_file(path: str = ".github/workflows/helix.yml") -> None:
    """Create GitHub Actions workflow file"""
    workflow = generate_github_actions_workflow()

    file_path = Path(path)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text(workflow)

    print(f"Created GitHub Actions workflow: {path}")


def create_gitlab_ci_file(path: str = ".gitlab-ci.yml") -> None:
    """Create GitLab CI configuration file"""
    workflow = generate_gitlab_ci_workflow()

    file_path = Path(path)
    file_path.write_text(workflow)

    print(f"Created GitLab CI configuration: {path}")


# GitHub App integration for PR comments
def create_pr_comment_body(
    checks_passed: List[str],
    checks_failed: List[str],
    summary: str = ""
) -> str:
    """Create PR comment body"""

    lines = [
        "## Helix CI Report",
        "",
    ]

    if checks_passed:
        lines.append("### Passed Checks")
        for check in checks_passed:
            lines.append(f"- ✅ {check}")
        lines.append("")

    if checks_failed:
        lines.append("### Failed Checks")
        for check in checks_failed:
            lines.append(f"- ❌ {check}")
        lines.append("")

    if summary:
        lines.append(summary)

    return "\n".join(lines)


# Status badge generation
def get_status_badge(url: str, status: str) -> str:
    """Generate status badge SVG"""
    colors = {
        "success": "#10B981",
        "failure": "#EF4444",
        "pending": "#F59E0B",
        "running": "#3B82F6",
    }

    color = colors.get(status, "#6B7280")

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="100" height="20">
  <rect width="100" height="20" fill="{color}" rx="4"/>
  <text x="50" y="14" fill="white" font-size="12" text-anchor="middle" font-family="sans-serif">{status.upper()}</text>
</svg>"""


# Quick reference for common CI/CD platforms
CI_PLATFORMS = {
    "github": {
        "config_path": ".github/workflows/helix.yml",
        "generator": generate_github_actions_workflow,
    },
    "gitlab": {
        "config_path": ".gitlab-ci.yml",
        "generator": generate_gitlab_ci_workflow,
    },
    "jenkins": {
        "config_path": "Jenkinsfile",
        "generator": None,  # Jenkinsfile is different format
    },
}
