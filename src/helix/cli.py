"""
Helix CLI Entry Point
"""

import asyncio
import sys
from pathlib import Path

import click
from rich.console import Console
from rich.table import Table
from rich.syntax import Syntax
from rich.markdown import Markdown
from rich.panel import Panel

from helix import __version__
from helix.core.orchestrator import HelixOrchestrator, HelixConfig
from helix.core.intent import Intent, IntentType
from helix.skills.spec import SpecSkill
from helix.skills.build import BuildSkill
from helix.skills.verify import VerifySkill
from helix.skills.review import ReviewSkill
from helix.skills.ship import ShipSkill
from helix.skills.qa import QASkill
from helix.skills.audit import AuditSkill
from helix.skills.gate import GateSkill
from helix.skills.base import SkillConfig

console = Console()


@click.group()
@click.version_option(version=__version__)
def main():
    """Project Helix - AI Era Software Engineering Methodology New Paradigm"""
    pass


@main.command()
@click.argument("input_text", required=False)
@click.option("--template", "-t", help="Specify template type (crud/api/algorithm/integration/ui/script/infrastructure)")
@click.option("--no-confirm", is_flag=True, help="Skip confirmation step")
@click.option("--output", "-o", type=click.Path(), help="Output file path")
def spec(input_text: str, template: str, no_confirm: bool, output: str):
    """Spec skill - Transform requirements into structured specification

    Usage:
        helix spec "I want to build a user login feature"
        helix spec "Create a user management API" --template api
        helix spec  # Interactive mode
    """
    if not input_text:
        console.print("[yellow]Entering interactive mode...[/yellow]")
        input_text = click.prompt("Describe the feature you want to build", type=str)

    console.print(f"\n[bold blue]⚡ Helix Spec[/bold blue] - Processing requirement")
    console.print(f"  Input: {input_text}\n")

    # Initialize skill
    skill_config = SkillConfig(auto_confirm=no_confirm)
    spec_skill = SpecSkill(skill_config)

    # Create intent
    intent = Intent(
        type=IntentType.SPEC,
        raw_input=input_text,
        confidence=0.9
    )

    # Execute skill
    try:
        result = asyncio.run(spec_skill.execute(intent, None))

        if result.success:
            console.print("[bold green]✓[/bold green] Specification generated\n")

            # Display generated Spec
            spec_content = result.data.get("spec_content", "")
            console.print(Panel(spec_content, title="Generated Specification", border_style="blue"))

            # Requirement type
            req_type = result.data.get("requirement_type", "general")
            console.print(f"[dim]Requirement type: {req_type}[/dim]\n")

            # Save to file
            if output:
                Path(output).write_text(spec_content)
                console.print(f"[green]✓[/green] Saved to: {output}")
            elif not no_confirm:
                # Confirm save
                save = click.confirm("Save to file?", default=True)
                if save:
                    filename = f"SPEC.md"
                    Path(filename).write_text(spec_content)
                    console.print(f"[green]✓[/green] Saved to: {filename}")
        else:
            console.print(f"[bold red]✗[/bold red] {result.message}")

    except Exception as e:
        console.print(f"[bold red]✗[/bold red] Execution error: {e}")
        sys.exit(1)


@main.command()
def templates():
    """List all available templates"""
    table = Table(title="Available Specification Templates")
    table.add_column("Template Name", style="cyan")
    table.add_column("Use Case", style="magenta")
    table.add_column("Description")

    templates = [
        ("crud", "CRUD Operations", "Data create/read/update/delete management"),
        ("api", "API Service", "REST/GraphQL interface"),
        ("algorithm", "Algorithm Implementation", "Sorting, search, recommendation, etc."),
        ("integration", "Third-party Integration", "External service integration"),
        ("ui", "Page/Component", "Frontend pages and components"),
        ("script", "Script Tool", "CLI tools and scripts"),
        ("infrastructure", "Infrastructure", "Deployment, CI/CD, etc."),
    ]

    for name, scenario, desc in templates:
        table.add_row(name, scenario, desc)

    console.print(table)


@main.command()
@click.argument("input", type=str, required=False)
@click.option("--framework", "-f", default="fastapi", help="Framework type (fastapi/django/express)")
@click.option("--output", "-o", default=".", help="Output directory")
@click.option("--dry-run", is_flag=True, help="Preview only, don't generate files")
@click.option("--llm", is_flag=True, help="Use LLM for enhanced code generation")
@click.option("--requirement", "-r", "requirement_text", help="Requirement description (instead of spec file)")
def build(input: str, framework: str, output: str, dry_run: bool, requirement_text: str, llm: bool):
    """Code skeleton generation - Generate code from specification or requirement

    Usage:
        helix build SPEC.md
        helix build SPEC.md --framework fastapi
        helix build "user login feature"
        helix build -r "user login feature"
        helix build "user login" --llm
    """
    # Determine if input is a file or requirement text
    spec_file = ""
    if input:
        input_path = Path(input)
        if input_path.exists() and input_path.is_file():
            spec_file = input
            display_input = spec_file
        else:
            # Treat as requirement text
            requirement_text = input
            display_input = requirement_text
    else:
        display_input = requirement_text or "N/A"

    console.print(f"\n[bold blue]⚡ Helix Build[/bold blue] - Generating code skeleton")
    console.print(f"  Input: {display_input[:50]}{'...' if len(display_input) > 50 else ''}")
    console.print(f"  Framework: {framework}")
    console.print(f"  Output: {output}\n")

    # Initialize skill
    build_skill = BuildSkill()

    # Create intent
    intent = Intent(
        type=IntentType.BUILD,
        raw_input=display_input,
        confidence=0.9,
        parameters={
            "spec_file": spec_file,
            "requirement": requirement_text,
            "framework": framework,
            "output": output,
            "use_llm": llm,
        }
    )

    # Execute skill
    try:
        result = asyncio.run(build_skill.execute(intent, None))

        if result.success:
            console.print("[bold green]✓[/bold green] Code skeleton generated\n")

            # Display generated files
            files = result.data.get("files", [])
            table = Table(title="Generated Files")
            table.add_column("File", style="cyan")
            table.add_column("Path", style="magenta")

            for f in files:
                table.add_row(f.split('/')[-1], f)

            console.print(table)

            console.print(f"\n[dim]Usage:[/dim]")
            console.print(f"  1. Install dependencies: pip install -r requirements.txt")
            console.print(f"  2. Start server: python main.py")
            console.print(f"  3. Run tests: pytest")
        else:
            console.print(f"[bold red]✗[/bold red] {result.message}")

    except Exception as e:
        console.print(f"[bold red]✗[/bold red] Execution error: {e}")
        import traceback
        console.print(f"[dim]{traceback.format_exc()}[/dim]")
        sys.exit(1)


@main.command()
@click.argument("path", default=".", required=False)
@click.option("--level", "-l", default="full",
              type=click.Choice(["static", "test", "acceptance", "full"]),
              help="Verification level")
def verify(path: str, level: str):
    """Automated verification - Run static checks, unit tests, acceptance tests

    Usage:
        helix verify
        helix verify ./src
        helix verify --level static
    """
    console.print(f"\n[bold blue]⚡ Helix Verify[/bold blue] - Running verification")
    console.print(f"  Path: {path}")
    console.print(f"  Level: {level}\n")

    # Initialize skill
    verify_skill = VerifySkill()

    # Create intent
    intent = Intent(
        type=IntentType.VERIFY,
        raw_input=path,
        confidence=0.9,
        parameters={
            "path": path,
            "level": level,
        }
    )

    # Execute skill
    try:
        result = asyncio.run(verify_skill.execute(intent, None))

        if result.success or "PARTIAL" in result.message or "partial" in result.message.lower():
            console.print(result.message)
        else:
            console.print(f"[bold red]✗[/bold red] Verification failed")
            console.print(result.message)

    except Exception as e:
        console.print(f"[bold red]✗[/bold red] Execution error: {e}")
        sys.exit(1)


@main.command()
@click.option("--base", "-b", default="main", help="Base branch to compare against")
@click.option("--path", "-p", default=".", help="Path to review")
def review(base: str, path: str):
    """Code review - Analyze changes for bugs, security issues, and quality problems

    Usage:
        helix review
        helix review --base main
        helix review --path src/
    """
    console.print(f"\n[bold blue]⚡ Helix Review[/bold blue] - Code review")
    console.print(f"  Base branch: {base}")
    console.print(f"  Path: {path}\n")

    # Initialize skill
    review_skill = ReviewSkill()

    # Create intent
    intent = Intent(
        type=IntentType.BUILD,
        raw_input=path,
        confidence=0.9,
        parameters={
            "path": path,
            "base": base,
        }
    )

    # Execute skill
    try:
        result = asyncio.run(review_skill.execute(intent, None))

        if result.success:
            console.print(result.message)

            # Show summary if there are findings
            if result.data.get("review_report"):
                report = result.data["review_report"]
                console.print("")
                console.print(f"[bold]Summary:[/bold]")
                console.print(f"  Files changed: {report.get('total_files', 0)}")
                console.print(f"  Lines changed: {report.get('total_lines_changed', 0)}")
                console.print(f"  Critical: [red]{report.get('critical', 0)}[/red]")
                console.print(f"  High: [yellow]{report.get('high', 0)}[/yellow]")
                console.print(f"  Medium: [blue]{report.get('medium', 0)}[/blue]")
                console.print(f"  Low: {report.get('low', 0)}")
        else:
            console.print(f"[bold red]✗[/bold red] {result.message}")

    except Exception as e:
        console.print(f"[bold red]✗[/bold red] Execution error: {e}")
        import traceback
        console.print(f"[dim]{traceback.format_exc()}[/dim]")
        sys.exit(1)


@main.command()
@click.option("--mode", "-m", default="create_pr",
              type=click.Choice(["create_pr", "merge", "deploy", "dry_run"]),
              help="Ship mode")
@click.option("--base", "-b", default="main", help="Base branch")
@click.option("--title", "-t", default="", help="PR title")
@click.option("--body", default="", help="PR body")
@click.option("--draft", is_flag=True, help="Create as draft PR")
@click.option("--auto-merge", is_flag=True, help="Auto-merge after CI passes")
@click.option("--bump-version", is_flag=True, help="Bump version before shipping")
@click.option("--version-type", default="patch",
              type=click.Choice(["major", "minor", "patch"]),
              help="Version bump type")
def ship(mode: str, base: str, title: str, body: str, draft: bool,
         auto_merge: bool, bump_version: bool, version_type: str):
    """Release and delivery - create PR, merge, tag, and deploy

    Usage:
        helix ship                    # Create PR
        helix ship --mode merge       # Create and merge PR
        helix ship --mode deploy      # Full pipeline with deploy
        helix ship --bump-version     # Bump version and ship
        helix ship --mode dry_run     # Preview only
    """
    console.print(f"\n[bold blue]⚡ Helix Ship[/bold blue] - Release & Delivery")
    console.print(f"  Mode: {mode}")
    console.print(f"  Base: {base}")
    console.print(f"  Bump version: {bump_version} ({version_type})\n")

    # Initialize skill
    ship_skill = ShipSkill()

    # Create intent
    intent = Intent(
        type=IntentType.BUILD,
        raw_input="ship",
        confidence=0.9,
        parameters={
            "mode": mode,
            "base": base,
            "title": title,
            "body": body,
            "draft": draft,
            "auto_merge": auto_merge,
            "bump_version": bump_version,
            "version_type": version_type,
        }
    )

    # Execute skill
    try:
        result = asyncio.run(ship_skill.execute(intent, None))

        if result.success:
            console.print(result.message)

            # Show logs
            if result.data.get("logs"):
                console.print("\n[dim]Logs:[/dim]")
                for log in result.data["logs"][:5]:
                    console.print(f"  [dim]{log}[/dim]")
        else:
            console.print(f"[bold red]✗[/bold red] {result.message}")

    except Exception as e:
        console.print(f"[bold red]✗[/bold red] Execution error: {e}")
        import traceback
        console.print(f"[dim]{traceback.format_exc()}[/dim]")
        sys.exit(1)


@main.command()
@click.option("--level", "-l", default="all",
              type=click.Choice(["unit", "integration", "e2e", "all"]),
              help="Test level")
@click.option("--path", "-p", default=".", help="Test path")
@click.option("--coverage", is_flag=True, help="Run with coverage")
@click.option("--fail-fast", is_flag=True, help="Stop on first failure")
def qa(level: str, path: str, coverage: bool, fail_fast: bool):
    """Testing automation - run tests, coverage analysis, and reports

    Usage:
        helix qa
        helix qa --level unit
        helix qa --coverage
        helix qa --level all --fail-fast
    """
    console.print(f"\n[bold blue]⚡ Helix QA[/bold blue] - Testing Automation")
    console.print(f"  Level: {level}")
    console.print(f"  Path: {path}")
    console.print(f"  Coverage: {coverage}\n")

    # Initialize skill
    qa_skill = QASkill()

    # Create intent
    intent = Intent(
        type=IntentType.BUILD,
        raw_input="qa",
        confidence=0.9,
        parameters={
            "level": level,
            "path": path,
            "coverage": coverage,
            "fail_fast": fail_fast,
        }
    )

    # Execute skill
    try:
        result = asyncio.run(qa_skill.execute(intent, None))

        if result.success:
            console.print(result.message)

            # Show summary
            if result.data.get("test_result"):
                tr = result.data["test_result"]
                console.print("\n[bold]Summary:[/bold]")
                console.print(f"  Passed:  [green]{tr['passed']}[/green]")
                console.print(f"  Failed:  [red]{tr['failed']}[/red]")
                console.print(f"  Duration: {tr['duration']:.2f}s")
                if tr.get('coverage'):
                    console.print(f"  Coverage: {tr['coverage']}%")
        else:
            console.print(f"[bold red]✗[/bold red] {result.message}")

            # Show failed tests
            if result.data.get("failed_tests"):
                console.print("\n[bold]Failed Tests:[/bold]")
                for test in result.data["failed_tests"][:3]:
                    console.print(f"  [red]✗[/red] {test['name']}")

    except Exception as e:
        console.print(f"[bold red]✗[/bold red] Execution error: {e}")
        import traceback
        console.print(f"[dim]{traceback.format_exc()}[/dim]")
        sys.exit(1)


@main.command()
@click.option("--security/--no-security", default=True, help="Run security audit")
@click.option("--dependencies/--no-dependencies", default=True, help="Run dependency audit")
@click.option("--architecture/--no-architecture", default=True, help="Run architecture audit")
@click.option("--compliance/--no-compliance", default=False, help="Run compliance audit")
@click.option("--path", "-p", default=".", help="Path to audit")
def audit(security: bool, dependencies: bool, architecture: bool, compliance: bool, path: str):
    """Security and architecture audit - vulnerability scanning, dependency check

    Usage:
        helix audit
        helix audit --security
        helix audit --dependencies
        helix audit --full
    """
    console.print(f"\n[bold blue]⚡ Helix Audit[/bold blue] - Security & Architecture Audit")
    console.print(f"  Security: {security}")
    console.print(f"  Dependencies: {dependencies}")
    console.print(f"  Architecture: {architecture}")
    console.print(f"  Compliance: {compliance}\n")

    # Initialize skill
    audit_skill = AuditSkill()

    # Create intent
    intent = Intent(
        type=IntentType.BUILD,
        raw_input="audit",
        confidence=0.9,
        parameters={
            "security": security,
            "dependencies": dependencies,
            "architecture": architecture,
            "compliance": compliance,
            "path": path,
        }
    )

    # Execute skill
    try:
        result = asyncio.run(audit_skill.execute(intent, None))

        if result.success:
            console.print(result.message)
        else:
            console.print(f"[bold red]✗[/bold red] {result.message}")

    except Exception as e:
        console.print(f"[bold red]✗[/bold red] Execution error: {e}")
        import traceback
        console.print(f"[dim]{traceback.format_exc()}[/dim]")
        sys.exit(1)


@main.command()
@click.option("--strict", is_flag=True, help="Strict mode - fail on warnings")
@click.option("--security/--no-security", default=True, help="Run security gate")
@click.option("--min-coverage", default=70.0, help="Minimum coverage percentage")
@click.option("--bypass", default="", help="Bypass gate with reason")
def gate(strict: bool, security: bool, min_coverage: float, bypass: str):
    """Quality gate - enforce quality thresholds before merge/deploy

    Usage:
        helix gate
        helix gate --strict
        helix gate --min-coverage 80
        helix gate --bypass "Critical security fix"
    """
    console.print(f"\n[bold blue]⚡ Helix Gate[/bold blue] - Quality Gate")
    console.print(f"  Strict: {strict}")
    console.print(f"  Security: {security}")
    console.print(f"  Min Coverage: {min_coverage}%\n")

    # Initialize skill
    gate_skill = GateSkill()

    # Create intent
    intent = Intent(
        type=IntentType.BUILD,
        raw_input="gate",
        confidence=0.9,
        parameters={
            "strict": strict,
            "security": security,
            "min_coverage": min_coverage,
            "bypass": bypass,
        }
    )

    # Execute skill
    try:
        result = asyncio.run(gate_skill.execute(intent, None))

        console.print(result.message)

        if not result.success:
            sys.exit(1)

    except Exception as e:
        console.print(f"[bold red]✗[/bold red] Execution error: {e}")
        import traceback
        console.print(f"[dim]{traceback.format_exc()}[/dim]")
        sys.exit(1)


@main.command()
@click.argument("url", required=False)
@click.option("--screenshot", is_flag=True, help="Take screenshot")
@click.option("--interactive", is_flag=True, help="Interactive mode")
@click.option("--action", default="navigate", help="Browser action")
def browse(url: str, screenshot: bool, interactive: bool, action: str):
    """Browser control - E2E testing, visual regression, site verification

    Usage:
        helix browse https://example.com
        helix browse https://example.com --screenshot
    """
    from helix.skills.browse import BrowseSkill

    console.print(f"\n[bold blue]⚡ Helix Browse[/bold blue] - Browser Control")
    console.print(f"  URL: {url or 'not provided'}")
    console.print(f"  Screenshot: {screenshot}")
    console.print(f"  Interactive: {interactive}\n")

    if not url:
        console.print("[yellow]URL is required[/yellow]")
        console.print("Usage: helix browse <url>")
        sys.exit(1)

    # Initialize skill
    browse_skill = BrowseSkill()

    # Create intent
    intent = Intent(
        type=IntentType.BUILD,
        raw_input="browse",
        confidence=0.9,
        parameters={
            "url": url,
            "action": action,
            "screenshot": screenshot,
            "interactive": interactive,
        }
    )

    # Execute skill
    try:
        result = asyncio.run(browse_skill.execute(intent, None))

        if result.success:
            console.print(result.message)
        else:
            console.print(f"[bold red]✗[/bold red] {result.message}")
            sys.exit(1)

    except Exception as e:
        console.print(f"[bold red]✗[/bold red] Execution error: {e}")
        import traceback
        console.print(f"[dim]{traceback.format_exc()}[/dim]")
        sys.exit(1)


@main.command()
@click.option("--brand", default="", help="Brand name")
@click.option("--template", default="default", help="Design template")
@click.option("--output", default="DESIGN.md", help="Output file")
def design(brand: str, template: str, output: str):
    """Design generation - design system, typography, color, layout

    Usage:
        helix design --brand "My Brand"
        helix design --template minimal
        helix design --output design.md
    """
    from helix.skills.design import DesignSkill

    console.print(f"\n[bold blue]⚡ Helix Design[/bold blue] - Design Generation")
    console.print(f"  Brand: {brand or 'default'}")
    console.print(f"  Template: {template}")
    console.print(f"  Output: {output}\n")

    # Initialize skill
    design_skill = DesignSkill()

    # Create intent
    intent = Intent(
        type=IntentType.BUILD,
        raw_input="design",
        confidence=0.9,
        parameters={
            "brand": brand,
            "template": template,
            "output": output,
        }
    )

    # Execute skill
    try:
        result = asyncio.run(design_skill.execute(intent, None))

        if result.success:
            console.print(result.message)
        else:
            console.print(f"[bold red]✗[/bold red] {result.message}")
            sys.exit(1)

    except Exception as e:
        console.print(f"[bold red]✗[/bold red] Execution error: {e}")
        import traceback
        console.print(f"[dim]{traceback.format_exc()}[/dim]")
        sys.exit(1)


@main.command()
@click.argument("command", default="show", required=False)
@click.option("--query", "-q", default="", help="Search query")
@click.option("--key", "-k", default="", help="Learning key")
@click.option("--insight", "-i", default="", help="Learning insight")
@click.option("--type", "-t", default="pattern", help="Learning type")
def learn(command: str, query: str, key: str, insight: str, type: str):
    """Continuous learning - project knowledge, learnings, patterns

    Usage:
        helix learn
        helix learn search --query <keyword>
        helix learn add --key <name> --insight <description>
        helix learn stats
    """
    from helix.skills.learn import LearnSkill

    console.print(f"\n[bold blue]⚡ Helix Learn[/bold blue] - Continuous Learning")
    console.print(f"  Command: {command}")
    console.print(f"  Query: {query or 'none'}\n")

    # Initialize skill
    learn_skill = LearnSkill()

    # Map CLI command to skill command
    command_map = {
        "search": "search",
        "stats": "stats",
        "add": "add",
        "show": "show",
    }
    skill_command = command_map.get(command, "show")

    # Create intent
    intent = Intent(
        type=IntentType.BUILD,
        raw_input="learn",
        confidence=0.9,
        parameters={
            "command": skill_command,
            "query": query,
            "key": key,
            "insight": insight,
            "type": type,
        }
    )

    # Execute skill
    try:
        result = asyncio.run(learn_skill.execute(intent, None))

        if result.success:
            console.print(result.message)
            # Show data if available
            if result.data:
                if "learnings" in result.data:
                    for learning in result.data.get("learnings", [])[:10]:
                        console.print(f"  • {learning.get('key')}: {learning.get('insight', '')[:50]}...")
                if "results" in result.data:
                    console.print(result.data["results"])
                if "total" in result.data:
                    console.print(f"  Total: {result.data['total']}")
                if "by_type" in result.data:
                    for t, count in result.data["by_type"].items():
                        console.print(f"  {t}: {count}")
        else:
            console.print(f"[bold red]✗[/bold red] {result.message}")
            sys.exit(1)

    except Exception as e:
        console.print(f"[bold red]✗[/bold red] Execution error: {e}")
        import traceback
        console.print(f"[dim]{traceback.format_exc()}[/dim]")
        sys.exit(1)


@main.command()
@click.argument("command", default="status", required=False)
@click.argument("label", default="", required=False)
@click.option("--id", "-i", default="", help="Checkpoint ID")
def checkpoint(command: str, label: str, id: str):
    """State persistence - save/restore, cross-session continuity

    Usage:
        helix checkpoint save "working on feature X"
        helix checkpoint list
        helix checkpoint restore <id>
        helix checkpoint status
    """
    from helix.skills.checkpoint import CheckpointSkill

    console.print(f"\n[bold blue]⚡ Helix Checkpoint[/bold blue] - State Persistence")
    console.print(f"  Command: {command}")
    console.print(f"  Label: {label or 'none'}\n")

    # Initialize skill
    checkpoint_skill = CheckpointSkill()

    # Map CLI command
    command_map = {
        "save": "save",
        "list": "list",
        "restore": "restore",
        "status": "status",
    }
    skill_command = command_map.get(command, "status")

    # Create intent
    intent = Intent(
        type=IntentType.BUILD,
        raw_input="checkpoint",
        confidence=0.9,
        parameters={
            "command": skill_command,
            "label": label,
            "id": id,
        }
    )

    # Execute skill
    try:
        result = asyncio.run(checkpoint_skill.execute(intent, None))

        if result.success:
            console.print(result.message)
            if result.data:
                if "checkpoints" in result.data:
                    for cp in result.data["checkpoints"]:
                        console.print(f"  • {cp.get('id')}: {cp.get('label')} ({cp.get('branch')})")
                if "latest" in result.data and result.data["latest"]:
                    latest = result.data["latest"]
                    console.print(f"\n[green]Latest checkpoint:[/green]")
                    console.print(f"  ID: {latest.get('id')}")
                    console.print(f"  Label: {latest.get('label')}")
                    console.print(f"  Branch: {latest.get('branch')}")
                    console.print(f"  Commit: {latest.get('commit')}")
                if "total" in result.data:
                    console.print(f"  Total: {result.data['total']}")
        else:
            console.print(f"[bold red]✗[/bold red] {result.message}")
            sys.exit(1)

    except Exception as e:
        console.print(f"[bold red]✗[/bold red] Execution error: {e}")
        import traceback
        console.print(f"[dim]{traceback.format_exc()}[/dim]")
        sys.exit(1)


@main.command()
@click.argument("input_text")
def classify(input_text: str):
    """Test requirement type recognition"""
    spec_skill = SpecSkill()
    req_type = spec_skill._classify_requirement(input_text)
    entities = spec_skill._extract_entities(input_text)

    console.print(f"\n[bold]Input:[/bold] {input_text}\n")
    console.print(f"[bold]Recognized type:[/bold] {req_type.value}")
    console.print(f"[bold]Extracted entities:[/bold]")
    console.print(f"  Domain: {entities.domain or '(not recognized)'}")
    console.print(f"  Action: {entities.action or '(not recognized)'}")
    console.print(f"  Integrations: {entities.integrations or 'none'}")


@main.command()
def list_skills():
    """List all available skills"""
    table = Table(title="Helix Available Skills")
    table.add_column("Name", style="cyan")
    table.add_column("Category", style="magenta")
    table.add_column("Status", style="green")
    table.add_column("Description")

    skills = [
        ("spec", "Execution Engine", "Stable ✅", "Spec - Requirement to specification"),
        ("build", "Execution Engine", "Stable ✅", "Build - Specification to code"),
        ("verify", "Execution Engine", "Stable ✅", "Verify - Automated verification"),
        ("ship", "Execution Engine", "Stable ✅", "Ship - Release & delivery"),
        ("review", "Quality Assurance", "Stable", "Review - Code review"),
        ("test", "Quality Assurance", "Stable ✅", "Test - Intelligent testing"),
        ("audit", "Quality Assurance", "Stable ✅", "Audit - Security audit"),
        ("gate", "Quality Assurance", "Stable ✅", "Gate - Quality gate"),
        ("browse", "Infrastructure", "Stable", "Browse - Browser control"),
        ("design", "Infrastructure", "Stable", "Design - Design generation"),
        ("learn", "Infrastructure", "Stable", "Learn - Continuous learning"),
        ("checkpoint", "Infrastructure", "Stable", "Checkpoint - State persistence"),
    ]

    for name, category, status, desc in skills:
        table.add_row(f"/{name}", category, status, desc)

    console.print(table)


@main.command()
def status():
    """View Project Helix status"""
    console.print(f"[bold]Project:[/bold] Helix")
    console.print(f"[bold]Version:[/bold] {__version__}")
    console.print("[bold]Status:[/bold] ✅ Stable")
    console.print("")
    console.print("[bold]Architecture:[/bold]")
    console.print("  - L4: Meta-Methodology + Platform")
    console.print("  - L3: Execution Engine + AI Engine")
    console.print("  - L2: Quality Assurance")
    console.print("  - L1: Infrastructure")
    console.print("")
    console.print("[bold]Skills:[/bold]")
    console.print("  - 12 skills across 4 layers")
    console.print("  - All skills operational")


@main.command()
def plugins():
    """List available plugins"""
    console.print(f"\n[bold blue]⚡ Helix Plugins[/bold blue]\n")

    try:
        from helix.plugins import get_plugin_manager
        manager = get_plugin_manager()
        manager.initialize()

        plugin_list = manager.list_plugins()

        if not plugin_list:
            console.print("[yellow]No plugins found[/yellow]")
            console.print("Plugins can be added to the plugins/ directory")
            return

        table = Table(title="Installed Plugins")
        table.add_column("Name", style="cyan")
        table.add_column("Version", style="magenta")
        table.add_column("Status", style="green")
        table.add_column("Description")

        for plugin in plugin_list:
            status_emoji = "✅" if plugin["status"] == "active" else "❌"
            table.add_row(
                plugin["name"],
                plugin["version"],
                f"{status_emoji} {plugin['status']}",
                plugin["description"][:50] if plugin["description"] else "",
            )

        console.print(table)

    except Exception as e:
        console.print(f"[yellow]Plugin system not available: {e}[/yellow]")


@main.command()
@click.option("--host", default="0.0.0.0", help="Host to bind to")
@click.option("--port", default=8080, help="Port to bind to")
def serve(host: str, port: int):
    """Start Helix API server

    Usage:
        helix serve
        helix serve --port 3000
    """
    console.print(f"\n[bold blue]⚡ Helix API Server[/bold blue]")
    console.print(f"  Host: {host}")
    console.print(f"  Port: {port}")
    console.print(f"  Docs: http://{host}:{port}/docs\n")

    try:
        from helix.api import run_server
        run_server(host=host, port=port)
    except ImportError:
        console.print("[red]Error: fastapi and uvicorn required[/red]")
        console.print("[dim]Install with: pip install helix[api][/dim]")
        sys.exit(1)


@main.command()
@click.argument("platform", default="github", type=click.Choice(["github", "gitlab"]))
@click.option("--path", "-p", default=None, help="Output path")
@click.option("--audit/--no-audit", default=True, help="Include security audit")
@click.option("--gate/--no-gate", default=True, help="Include quality gate")
def ci(platform: str, path: str, audit: bool, gate: bool):
    """Generate CI/CD configuration

    Usage:
        helix ci github
        helix ci gitlab
    """
    console.print(f"\n[bold blue]⚡ Helix CI/CD Setup[/bold blue]")
    console.print(f"  Platform: {platform}")
    console.print(f"  Audit: {audit}")
    console.print(f"  Gate: {gate}\n")

    try:
        if platform == "github":
            from helix.ci import create_github_actions_file
            output_path = path or ".github/workflows/helix.yml"
            create_github_actions_file(output_path)
        else:
            from helix.ci import create_gitlab_ci_file
            output_path = path or ".gitlab-ci.yml"
            create_gitlab_ci_file(output_path)

        console.print(f"[green]✓ Created CI/CD configuration: {output_path}[/green]")

    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        sys.exit(1)


@main.command()
@click.option("--output", "-o", default=".", help="Output directory")
def docs(output: str):
    """Generate project documentation

    Usage:
        helix docs
        helix docs --output ./docs
    """
    console.print(f"\n[bold blue]⚡ Helix Documentation[/bold blue]")
    console.print(f"  Output: {output}\n")

    try:
        from helix.docs import run_docs_generator
        run_docs_generator(output)
        console.print(f"[green]✓ Documentation generated successfully[/green]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        sys.exit(1)


@main.command()
def metrics():
    """Show performance metrics

    Usage:
        helix metrics
    """
    console.print(f"\n[bold blue]⚡ Helix Performance Metrics[/bold blue]\n")

    try:
        from helix.monitoring import get_performance_monitor

        monitor = get_performance_monitor()
        metrics = monitor.get_metrics()
        health = monitor.get_health_status()

        console.print(f"[bold]Health Status:[/bold] {health['status'].upper()}")
        console.print(f"[bold]Uptime:[/bold] {health['uptime_seconds']:.1f}s")
        console.print("")
        console.print(f"[bold]Total Requests:[/bold] {metrics.total_requests}")
        console.print(f"[bold]Success Rate:[/bold] {health['success_rate']*100:.1f}%")
        console.print(f"[bold]Avg Latency:[/bold] {metrics.avg_latency_ms:.1f}ms")
        console.print(f"[bold]P95 Latency:[/bold] {metrics.p95_latency_ms:.1f}ms")
        console.print(f"[bold]P99 Latency:[/bold] {metrics.p99_latency_ms:.1f}ms")

        # Show per-skill metrics
        skill_metrics = monitor.get_all_skill_metrics()
        if skill_metrics:
            console.print("\n[bold]Per-Skill Metrics:[/bold]")
            for sm in skill_metrics:
                if sm:
                    console.print(f"  {sm['skill']}: {sm['total_requests']} requests, "
                                  f"{sm['avg_latency_ms']:.1f}ms avg")

    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        console.print("[yellow]Run some skills first to collect metrics[/yellow]")


if __name__ == "__main__":
    main()
