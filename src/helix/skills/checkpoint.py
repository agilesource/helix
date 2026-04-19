"""
Helix Checkpoint Skill - State Persistence

Helix-native state management:
- Save/restore working state
- Cross-session continuity
- Decision capture
- Remaining work tracking
- Git state integration
"""

import json
from pathlib import Path
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, asdict
from datetime import datetime

from helix.skills.base import Skill, SkillResult, SkillConfig, SkillCategory, SkillStatus
from helix.core.intent import Intent, IntentType
from helix.core.context import HelixContext


@dataclass
class Checkpoint:
    """Checkpoint entry"""
    id: str
    label: str
    description: str
    timestamp: str
    branch: str
    commit: str
    status: str
    cwd: str
    remaining_work: List[str]
    decisions: List[str]
    tags: List[str]


class CheckpointSkill(Skill):
    """
    Checkpoint Skill - State Persistence

    Helix-native cross-session state management
    """

    name = "checkpoint"
    description = "State persistence - save/restore, cross-session continuity"
    category = SkillCategory.INFRASTRUCTURE
    status = SkillStatus.STABLE

    examples = [
        "helix checkpoint save 'working on feature X'",
        "helix checkpoint list",
        "helix checkpoint restore <id>",
        "helix checkpoint status",
    ]

    def __init__(self, config: Optional[SkillConfig] = None):
        super().__init__(config)
        self.checkpoint_dir: Optional[Path] = None
        self._initialize_storage()

    def _do_initialize(self) -> None:
        """Initialize checkpoint skill"""
        self._initialize_storage()

    def _initialize_storage(self) -> None:
        """Initialize storage directory"""
        project_root = Path.cwd()
        helix_dir = project_root / ".helix" / "checkpoints"
        helix_dir.mkdir(parents=True, exist_ok=True)
        self.checkpoint_dir = helix_dir

    def _get_git_info(self) -> Dict[str, str]:
        """Get current git status"""
        import subprocess

        info = {
            "branch": "unknown",
            "commit": "unknown",
            "status": "",
        }

        try:
            # Branch
            result = subprocess.run(
                ["git", "branch", "--show-current"],
                capture_output=True, text=True, cwd=Path.cwd()
            )
            if result.returncode == 0:
                info["branch"] = result.stdout.strip()

            # Commit
            result = subprocess.run(
                ["git", "rev-parse", "--short", "HEAD"],
                capture_output=True, text=True, cwd=Path.cwd()
            )
            if result.returncode == 0:
                info["commit"] = result.stdout.strip()

            # Status
            result = subprocess.run(
                ["git", "status", "--porcelain"],
                capture_output=True, text=True, cwd=Path.cwd()
            )
            if result.returncode == 0:
                info["status"] = result.stdout.strip()

        except Exception:
            pass

        return info

    async def execute(self, intent: Intent, context: Optional[HelixContext]) -> SkillResult:
        """Execute checkpoint skill"""
        import time
        start_time = time.time()

        params = intent.parameters
        command = params.get("command", "status")
        label = params.get("label", "")
        checkpoint_id = params.get("id", "")
        description = params.get("description", "")
        remaining = params.get("remaining", [])
        decisions = params.get("decisions", [])
        tags = params.get("tags", [])

        try:
            if command == "save":
                result = await self._save_checkpoint(label, description, remaining, decisions, tags)
            elif command == "list":
                result = await self._list_checkpoints()
            elif command == "restore":
                result = await self._restore_checkpoint(checkpoint_id)
            elif command == "delete":
                result = await self._delete_checkpoint(checkpoint_id)
            else:
                result = await self._show_status()

            execution_time = int((time.time() - start_time) * 1000)

            return SkillResult(
                success=result["success"],
                message=result["message"],
                data=result.get("data", {}),
                execution_time_ms=execution_time,
            )

        except Exception as e:
            return SkillResult(
                success=False,
                message=f"Checkpoint failed: {str(e)}",
                errors=[str(e)]
            )

    async def _save_checkpoint(
        self, label: str, description: str, remaining: List[str],
        decisions: List[str], tags: List[str]
    ) -> Dict[str, Any]:
        """Save a checkpoint"""
        if not label:
            label = "Auto checkpoint"

        # Get git info
        git_info = self._get_git_info()

        # Create checkpoint
        checkpoint = Checkpoint(
            id=datetime.now().strftime("%Y%m%d-%H%M%S"),
            label=label,
            description=description,
            timestamp=datetime.now().isoformat(),
            branch=git_info["branch"],
            commit=git_info["commit"],
            status=git_info["status"],
            cwd=str(Path.cwd()),
            remaining_work=remaining,
            decisions=decisions,
            tags=tags
        )

        # Save to file
        assert self.checkpoint_dir is not None
        checkpoint_file = self.checkpoint_dir / f"{checkpoint.id}.json"
        checkpoint_file.write_text(json.dumps(asdict(checkpoint), indent=2))

        return {
            "success": True,
            "message": f"Checkpoint saved: {checkpoint.id}",
            "data": {
                "id": checkpoint.id,
                "label": checkpoint.label,
                "branch": checkpoint.branch,
                "commit": checkpoint.commit
            }
        }

    async def _list_checkpoints(self) -> Dict[str, Any]:
        """List all checkpoints"""
        if not self.checkpoint_dir or not self.checkpoint_dir.exists():
            return {
                "success": True,
                "message": "No checkpoints yet",
                "data": {"checkpoints": []}
            }

        try:
            checkpoints = []
            for f in sorted(self.checkpoint_dir.glob("*.json"), reverse=True):
                data = json.loads(f.read_text())
                checkpoints.append({
                    "id": data.get("id"),
                    "label": data.get("label"),
                    "description": data.get("description", ""),
                    "timestamp": data.get("timestamp"),
                    "branch": data.get("branch"),
                    "commit": data.get("commit"),
                    "remaining_work": data.get("remaining_work", []),
                    "decisions": data.get("decisions", []),
                    "tags": data.get("tags", [])
                })

            return {
                "success": True,
                "message": f"Found {len(checkpoints)} checkpoints",
                "data": {"checkpoints": checkpoints}
            }

        except Exception as e:
            return {
                "success": False,
                "message": str(e),
                "data": {"error": str(e)}
            }

    async def _restore_checkpoint(self, checkpoint_id: str) -> Dict[str, Any]:
        """Restore a checkpoint"""
        if not self.checkpoint_dir:
            return {
                "success": False,
                "message": "Checkpoint directory not available",
                "data": {}
            }

        try:
            checkpoint_file = self.checkpoint_dir / f"{checkpoint_id}.json"

            if not checkpoint_file.exists():
                return {
                    "success": False,
                    "message": f"Checkpoint not found: {checkpoint_id}",
                    "data": {}
                }

            data = json.loads(checkpoint_file.read_text())

            # Note: Full restore would need to restore git state
            # For now, show the checkpoint info with restoration guidance

            return {
                "success": True,
                "message": f"Checkpoint loaded: {checkpoint_id}",
                "data": {
                    "id": data.get("id"),
                    "label": data.get("label"),
                    "description": data.get("description"),
                    "branch": data.get("branch"),
                    "commit": data.get("commit"),
                    "timestamp": data.get("timestamp"),
                    "cwd": data.get("cwd"),
                    "remaining_work": data.get("remaining_work", []),
                    "decisions": data.get("decisions", []),
                    "restore_note": f"Run: git checkout {data.get('branch')} to restore branch state"
                }
            }

        except Exception as e:
            return {
                "success": False,
                "message": str(e),
                "data": {"error": str(e)}
            }

    async def _delete_checkpoint(self, checkpoint_id: str) -> Dict[str, Any]:
        """Delete a checkpoint"""
        if not self.checkpoint_dir:
            return {
                "success": False,
                "message": "Checkpoint directory not available",
                "data": {}
            }

        try:
            checkpoint_file = self.checkpoint_dir / f"{checkpoint_id}.json"

            if not checkpoint_file.exists():
                return {
                    "success": False,
                    "message": f"Checkpoint not found: {checkpoint_id}",
                    "data": {}
                }

            checkpoint_file.unlink()

            return {
                "success": True,
                "message": f"Checkpoint deleted: {checkpoint_id}",
                "data": {"id": checkpoint_id}
            }

        except Exception as e:
            return {
                "success": False,
                "message": str(e),
                "data": {"error": str(e)}
            }

    async def _show_status(self) -> Dict[str, Any]:
        """Show current checkpoint status"""
        git_info = self._get_git_info()

        if not self.checkpoint_dir or not self.checkpoint_dir.exists():
            return {
                "success": True,
                "message": "No checkpoint directory",
                "data": {
                    "branch": git_info["branch"],
                    "commit": git_info["commit"],
                    "checkpoints": 0
                }
            }

        checkpoints = list(self.checkpoint_dir.glob("*.json"))
        latest = None
        if checkpoints:
            latest = sorted(checkpoints, key=lambda f: f.stat().st_mtime, reverse=True)[0]
            latest_data = json.loads(latest.read_text())

        return {
            "success": True,
            "message": f"Checkpoint status",
            "data": {
                "total": len(checkpoints),
                "latest": latest_data if latest else None,
                "branch": git_info["branch"],
                "commit": git_info["commit"],
                "status": git_info["status"],
                "directory": str(self.checkpoint_dir)
            }
        }
