"""
Helix Learn Skill - Continuous Learning

Helix-native knowledge management:
- Project learnings capture and search
- Pattern discovery
- Cross-session knowledge graph
- Decision traceability
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
class Learning:
    """Learning entry"""
    id: str
    key: str
    insight: str
    learn_type: str  # pattern, pitfall, preference, architecture, tool, operational
    confidence: int  # 1-10
    source: str  # observed, user-stated, inferred, cross-model
    files: List[str]
    timestamp: str
    project: str = ""


class LearnSkill(Skill):
    """
    Learn Skill - Continuous Learning

    Helix-native project knowledge management
    """

    name = "learn"
    description = "Continuous learning - project knowledge, learnings, patterns"
    category = SkillCategory.INFRASTRUCTURE
    status = SkillStatus.STABLE

    examples = [
        "helix learn",
        "helix learn search <query>",
        "helix learn add --key pattern-name --insight 'description'",
        "helix learn stats",
    ]

    def __init__(self, config: Optional[SkillConfig] = None):
        super().__init__(config)
        self.learnings_file: Optional[Path] = None
        self._initialize_storage()

    def _do_initialize(self) -> None:
        """Initialize learn skill"""
        self._initialize_storage()

    def _initialize_storage(self) -> None:
        """Initialize storage directory"""
        # Find project root
        project_root = Path.cwd()
        project_name = project_root.name

        # Create .helix directory for learnings
        helix_dir = project_root / ".helix"
        helix_dir.mkdir(exist_ok=True)

        self.learnings_file = helix_dir / "learnings.jsonl"

    async def execute(self, intent: Intent, context: Optional[HelixContext]) -> SkillResult:
        """Execute learn skill"""
        import time
        start_time = time.time()

        params = intent.parameters
        command = params.get("command", "show")
        query = params.get("query", "")
        key = params.get("key", "")
        insight = params.get("insight", "")
        learn_type = params.get("type", "pattern")
        files = params.get("files", [])

        try:
            if command == "add":
                result = await self._add_learning(key, insight, learn_type, files)
            elif command == "search":
                result = await self._search_learnings(query)
            elif command == "stats":
                result = await self._show_stats()
            elif command == "export":
                result = await self._export_learnings()
            else:
                result = await self._show_recent()

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
                message=f"Learn failed: {str(e)}",
                errors=[str(e)]
            )

    def _load_learnings(self) -> List[Learning]:
        """Load all learnings from file"""
        if not self.learnings_file or not self.learnings_file.exists():
            return []

        learnings = []
        for line in self.learnings_file.read_text().strip().split("\n"):
            if line:
                try:
                    data = json.loads(line)
                    learnings.append(Learning(**data))
                except Exception:
                    pass

        return learnings

    def _save_learning(self, learning: Learning) -> None:
        """Save a learning to file"""
        if not self.learnings_file:
            return

        with open(self.learnings_file, "a") as f:
            f.write(json.dumps(asdict(learning), ensure_ascii=False) + "\n")

    def _deduplicate_learnings(self) -> List[Learning]:
        """Deduplicate learnings by key, keeping latest"""
        learnings = self._load_learnings()
        seen = {}

        for learning in learnings:
            key = f"{learning.key}|{learning.learn_type}"
            if key not in seen or learning.timestamp > seen[key].timestamp:
                seen[key] = learning

        return list(seen.values())

    async def _add_learning(
        self, key: str, insight: str, learn_type: str, files: List[str]
    ) -> Dict[str, Any]:
        """Add a learning entry"""
        if not key or not insight:
            return {
                "success": False,
                "message": "Key and insight are required",
                "data": {}
            }

        # Get project name
        project_name = Path.cwd().name

        learning = Learning(
            id=f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{hash(key) % 10000}",
            key=key,
            insight=insight,
            learn_type=learn_type,
            confidence=8,  # Default confidence
            source="user-stated",
            files=files,
            timestamp=datetime.now().isoformat(),
            project=project_name
        )

        self._save_learning(learning)

        return {
            "success": True,
            "message": f"Learning added: {key}",
            "data": {
                "key": key,
                "insight": insight,
                "type": learn_type
            }
        }

    async def _search_learnings(self, query: str) -> Dict[str, Any]:
        """Search learnings"""
        if not query:
            return await self._show_recent()

        learnings = self._deduplicate_learnings()

        # Search in key and insight
        query_lower = query.lower()
        results = [
            learning for learning in learnings
            if query_lower in learning.key.lower() or query_lower in learning.insight.lower()
        ]

        return {
            "success": True,
            "message": f"Found {len(results)} learnings matching '{query}'",
            "data": {
                "results": [asdict(l) for l in results[:20]],
                "query": query,
                "total": len(results)
            }
        }

    async def _show_stats(self) -> Dict[str, Any]:
        """Show learnings statistics"""
        learnings = self._deduplicate_learnings()

        by_type = {}
        by_source = {}
        by_project = {}

        for learning in learnings:
            by_type[learning.learn_type] = by_type.get(learning.learn_type, 0) + 1
            by_source[learning.source] = by_source.get(learning.source, 0) + 1
            by_project[learning.project] = by_project.get(learning.project, 0) + 1

        return {
            "success": True,
            "message": f"Total unique learnings: {len(learnings)}",
            "data": {
                "total": len(learnings),
                "by_type": by_type,
                "by_source": by_source,
                "by_project": by_project,
                "file": str(self.learnings_file) if self.learnings_file else None
            }
        }

    async def _show_recent(self) -> Dict[str, Any]:
        """Show recent learnings"""
        learnings = self._deduplicate_learnings()

        # Sort by timestamp descending
        sorted_learnings = sorted(learnings, key=lambda x: x.timestamp, reverse=True)
        recent = sorted_learnings[:20]

        return {
            "success": True,
            "message": f"Recent {len(recent)} learnings (total: {len(learnings)})",
            "data": {
                "learnings": [asdict(l) for l in recent],
                "total": len(learnings)
            }
        }

    async def _export_learnings(self) -> Dict[str, Any]:
        """Export learnings as markdown"""
        learnings = self._deduplicate_learnings()

        # Group by type
        by_type = {}
        for learning in learnings:
            if learning.learn_type not in by_type:
                by_type[learning.learn_type] = []
            by_type[learning.learn_type].append(learning)

        # Generate markdown
        lines = [
            "# Project Learnings",
            "",
            f"> Exported by Helix on {datetime.now().isoformat()}",
            "",
            f"Total: {len(learnings)} learnings",
            "",
        ]

        for learn_type, items in by_type.items():
            lines.append(f"## {learn_type.title()}")
            lines.append("")
            for item in items:
                lines.append(f"- **{item.key}**: {item.insight} (confidence: {item.confidence}/10)")
            lines.append("")

        content = "\n".join(lines)

        # Write to file
        export_file = Path(".helix") / "learnings_export.md"
        export_file.write_text(content)

        return {
            "success": True,
            "message": f"Exported {len(learnings)} learnings to {export_file}",
            "data": {
                "file": str(export_file),
                "total": len(learnings)
            }
        }
