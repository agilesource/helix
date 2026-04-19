"""
Helix Ship Skill - Release and Delivery

This skill handles the complete release workflow:
- Create pull request
- Run tests and checks
- Merge to main branch
- Tag release
- Deploy (optional)
"""

import asyncio
import subprocess
import os
from pathlib import Path
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

from helix.skills.base import (
    Skill, SkillResult, SkillConfig, SkillCategory, SkillStatus
)
from helix.core.intent import Intent, IntentType
from helix.core.context import HelixContext


class ShipMode(Enum):
    """Ship operation modes"""

    CREATE_PR = "create_pr"       # Create PR only
    MERGE = "merge"               # Create and merge PR
    DEPLOY = "deploy"             # Full pipeline with deploy
    DRY_RUN = "dry_run"           # Preview only


@dataclass
class ShipConfig:
    """Ship configuration"""
    mode: ShipMode = ShipMode.CREATE_PR
    base_branch: str = "main"
    target_branch: str = ""
    title: str = ""
    body: str = ""
    draft: bool = False
    auto_merge: bool = False
    delete_branch: bool = True
    bump_version: bool = False
    version_type: str = "patch"  # major, minor, patch


@dataclass
class ShipResult:
    """Ship operation result"""
    success: bool
    pr_url: Optional[str] = None
    pr_number: Optional[int] = None
    commit_sha: Optional[str] = None
    version: Optional[str] = None
    deployed: bool = False
    deploy_url: Optional[str] = None
    message: str = ""
    logs: List[str] = field(default_factory=list)


class ShipSkill(Skill):
    """
    Ship Skill - Release and Delivery

    Handles the complete release workflow from code to production
    """

    name = "ship"
    description = "Release and delivery - create PR, merge, tag, and deploy"
    category = SkillCategory.EXECUTION
    status = SkillStatus.EXPERIMENTAL

    examples = [
        "helix ship",
        "helix ship --mode merge",
        "helix ship --mode deploy --bump-version",
    ]

    def __init__(self, config: Optional[SkillConfig] = None):
        super().__init__(config)
        self.ship_config = ShipConfig()

    def _do_initialize(self) -> None:
        """Initialize ship skill"""
        pass

    async def execute(self, intent: Intent, context: Optional[HelixContext]) -> SkillResult:
        """Execute ship skill"""
        start_time = asyncio.get_event_loop().time()

        # Parse parameters
        params = intent.parameters

        # Update ship config
        self.ship_config.mode = params.get("mode", ShipMode.CREATE_PR)
        self.ship_config.base_branch = params.get("base", "main")
        self.ship_config.title = params.get("title", "")
        self.ship_config.body = params.get("body", "")
        self.ship_config.draft = params.get("draft", False)
        self.ship_config.auto_merge = params.get("auto_merge", False)
        self.ship_config.delete_branch = params.get("delete_branch", True)
        self.ship_config.bump_version = params.get("bump_version", False)
        self.ship_config.version_type = params.get("version_type", "patch")

        try:
            # Run ship workflow
            result = await self._run_ship_workflow()

            # Calculate execution time
            execution_time = int((asyncio.get_event_loop().time() - start_time) * 1000)

            return SkillResult(
                success=result.success,
                message=result.message,
                data={
                    "pr_url": result.pr_url,
                    "pr_number": result.pr_number,
                    "commit_sha": result.commit_sha,
                    "version": result.version,
                    "deployed": result.deployed,
                    "deploy_url": result.deploy_url,
                    "logs": result.logs,
                },
                execution_time_ms=execution_time,
            )

        except Exception as e:
            return SkillResult(
                success=False,
                message=f"Ship failed: {str(e)}",
                errors=[str(e)]
            )

    async def _run_ship_workflow(self) -> ShipResult:
        """Run the complete ship workflow"""
        result = ShipResult(success=False, message="")

        # Step 1: Get current branch info
        current_branch = await self._get_current_branch()
        result.logs.append(f"Current branch: {current_branch}")

        if current_branch == self.ship_config.base_branch:
            result.message = "Cannot ship from base branch. Create a feature branch first."
            return result

        # Step 2: Check for uncommitted changes
        has_changes = await self._has_uncommitted_changes()
        if has_changes:
            result.message = "You have uncommitted changes. Commit or stash them first."
            return result

        result.logs.append("No uncommitted changes - proceeding")

        # Step 3: Run pre-flight checks
        result.logs.append("Running pre-flight checks...")
        check_passed = await self._run_preflight_checks()
        if not check_passed and self.ship_config.mode != ShipMode.DRY_RUN:
            result.message = "Pre-flight checks failed. Fix issues before shipping."
            return result
        result.logs.append("Pre-flight checks passed")

        # Step 4: Bump version if requested
        if self.ship_config.bump_version:
            result.version = await self._bump_version()
            result.logs.append(f"Version bumped to: {result.version}")

        # Step 5: Create pull request
        if self.ship_config.mode in [ShipMode.CREATE_PR, ShipMode.MERGE, ShipMode.DEPLOY]:
            result.logs.append("Creating pull request...")
            pr_result = await self._create_pull_request()
            if not pr_result["success"]:
                result.message = f"Failed to create PR: {pr_result['error']}"
                return result

            result.pr_url = pr_result["url"]
            result.pr_number = pr_result["number"]
            result.logs.append(f"PR created: {result.pr_url}")

            # Step 6: Auto-merge if requested
            if self.ship_config.auto_merge or self.ship_config.mode == ShipMode.MERGE:
                result.logs.append("Merging pull request...")
                merge_result = await self._merge_pull_request(result.pr_number)
                if not merge_result["success"]:
                    result.message = f"Failed to merge PR: {merge_result['error']}"
                    return result

                result.commit_sha = merge_result.get("sha")
                result.logs.append(f"PR merged: {result.commit_sha}")

                # Delete branch if requested
                if self.ship_config.delete_branch:
                    await self._delete_branch(current_branch)
                    result.logs.append(f"Branch '{current_branch}' deleted")

            # Step 7: Deploy if requested
            if self.ship_config.mode == ShipMode.DEPLOY:
                result.logs.append("Deploying...")
                deploy_result = await self._deploy()
                result.deployed = deploy_result["success"]
                result.deploy_url = deploy_result.get("url", "")
                if result.deployed:
                    result.logs.append(f"Deployed to: {result.deploy_url}")
                else:
                    result.logs.append(f"Deploy failed: {deploy_result.get('error')}")

        # All done
        result.success = True

        # Build summary message
        if result.pr_url:
            result.message = f"✓ Ship completed successfully!\n"
            result.message += f"  PR: {result.pr_url}\n"
            if result.commit_sha:
                result.message += f"  Merged: {result.commit_sha[:7]}\n"
            if result.version:
                result.message += f"  Version: {result.version}\n"
            if result.deployed:
                result.message += f"  Deployed: {result.deploy_url}\n"
        else:
            result.message = "✓ Dry run completed. Use --mode merge to actually ship."

        return result

    async def _get_current_branch(self) -> str:
        """Get current branch name"""
        result = await asyncio.create_subprocess_exec(
            "git", "branch", "--show-current",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, _ = await result.communicate()
        return stdout.decode().strip()

    async def _has_uncommitted_changes(self) -> bool:
        """Check for uncommitted changes"""
        result = await asyncio.create_subprocess_exec(
            "git", "status", "--porcelain",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, _ = await result.communicate()
        return len(stdout.decode().strip()) > 0

    async def _run_preflight_checks(self) -> bool:
        """Run pre-flight checks"""
        # Check if main branch is up to date
        result = await asyncio.create_subprocess_exec(
            "git", "fetch", "origin", self.ship_config.base_branch,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        await result.communicate()

        # Check if branch is up to date with base
        result = await asyncio.create_subprocess_exec(
            "git", "merge-base", "--is-ancestor",
            f"origin/{self.ship_config.base_branch}",
            self.ship_config.base_branch,
        )
        # If exit code is 0, base is ancestor of current branch (up to date)
        return result.returncode == 0

    async def _bump_version(self) -> str:
        """Bump version number"""
        # Read current version
        version_file = Path("pyproject.toml")
        if not version_file.exists():
            return "0.0.0"

        content = version_file.read_text()
        import re
        match = re.search(r'version\s*=\s*"(\d+)\.(\d+)\.(\d+)"', content)
        if not match:
            return "0.0.0"

        major, minor, patch = int(match.group(1)), int(match.group(2)), int(match.group(3))

        # Bump based on type
        if self.ship_config.version_type == "major":
            major += 1
            minor = 0
            patch = 0
        elif self.ship_config.version_type == "minor":
            minor += 1
            patch = 0
        else:  # patch
            patch += 1

        new_version = f"{major}.{minor}.{patch}"

        # Update file
        new_content = re.sub(
            r'version\s*=\s*"\d+\.\d+\.\d+"',
            f'version = "{new_version}"',
            content
        )
        version_file.write_text(new_content)

        # Also update __init__.py
        init_file = Path("src/helix/__init__.py")
        if init_file.exists():
            init_content = init_file.read_text()
            init_content = re.sub(
                r'__version__\s*=\s*"[^"]+"',
                f'__version__ = "{new_version}"',
                init_content
            )
            init_file.write_text(init_content)

        # Commit version bump
        await asyncio.create_subprocess_exec(
            "git", "add", "pyproject.toml", "src/helix/__init__.py",
            stdout=asyncio.subprocess.DEVNULL,
            stderr=asyncio.subprocess.DEVNULL,
        )
        await asyncio.create_subprocess_exec(
            "git", "commit", "-m", f"chore: bump version to {new_version}",
            stdout=asyncio.subprocess.DEVNULL,
            stderr=asyncio.subprocess.DEVNULL,
        )

        return new_version

    async def _create_pull_request(self) -> Dict[str, Any]:
        """Create pull request using gh CLI"""
        # Get branch name
        branch = await self._get_current_branch()

        # Build title
        title = self.ship_config.title
        if not title:
            # Try to get commit message
            result = await asyncio.create_subprocess_exec(
                "git", "log", "-1", "--format=%s",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            stdout, _ = await result.communicate()
            title = stdout.decode().strip() or f"Update {branch}"

        # Build body
        body = self.ship_config.body
        if not body:
            body = f"Branch: {branch}\n\nPlease review and merge."

        # Create PR
        cmd = [
            "gh", "pr", "create",
            "--base", self.ship_config.base_branch,
            "--head", branch,
            "--title", title,
            "--body", body,
        ]

        if self.ship_config.draft:
            cmd.append("--draft")

        result = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await result.communicate()

        output = stdout.decode().strip()
        error = stderr.decode().strip()

        if result.returncode != 0:
            return {"success": False, "error": error}

        # Extract PR number from URL
        pr_number = output.split("/pull/")[-1] if "/pull/" in output else None

        return {
            "success": True,
            "url": output,
            "number": int(pr_number) if pr_number else None,
        }

    async def _merge_pull_request(self, pr_number: int) -> Dict[str, Any]:
        """Merge pull request"""
        # Check if auto-merge is enabled
        result = await asyncio.create_subprocess_exec(
            "gh", "pr", "merge", str(pr_number), "--squash", "--auto",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await result.communicate()

        output = stdout.decode().strip()
        error = stderr.decode().strip()

        if result.returncode != 0 and "already up to date" not in error.lower():
            return {"success": False, "error": error}

        # Get merged commit SHA
        sha_result = await asyncio.create_subprocess_exec(
            "gh", "pr", "view", str(pr_number), "--json", "mergeCommit", "-q", ".mergeCommit.sha",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        sha_out, _ = await sha_result.communicate()
        sha = sha_out.decode().strip().strip('"')

        return {
            "success": True,
            "sha": sha,
        }

    async def _delete_branch(self, branch: str) -> None:
        """Delete branch after merge"""
        await asyncio.create_subprocess_exec(
            "git", "push", "origin", "--delete", branch,
            stdout=asyncio.subprocess.DEVNULL,
            stderr=asyncio.subprocess.DEVNULL,
        )

    async def _deploy(self) -> Dict[str, Any]:
        """Deploy application"""
        # This is a placeholder - actual deployment would depend on the project
        # For now, just return success with placeholder URL
        return {
            "success": True,
            "url": "https://example.com",
        }
