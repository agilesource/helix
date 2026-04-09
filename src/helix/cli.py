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
from helix.skills.base import SkillConfig

console = Console()


@click.group()
@click.version_option(version=__version__)
def main():
    """Helix - AI Era Software Engineering Methodology New Paradigm"""
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
@click.argument("spec_file", type=click.Path(exists=True))
@click.option("--framework", "-f", default="fastapi", help="Framework type (fastapi/django/express)")
@click.option("--output", "-o", default=".", help="Output directory")
@click.option("--dry-run", is_flag=True, help="Preview only, don't generate files")
def build(spec_file: str, framework: str, output: str, dry_run: bool):
    """Code skeleton generation - Generate code from specification

    Usage:
        helix build SPEC.md
        helix build SPEC.md --framework fastapi
        helix build SPEC.md -o ./src
    """
    console.print(f"\n[bold blue]⚡ Helix Build[/bold blue] - Generating code skeleton")
    console.print(f"  Specification: {spec_file}")
    console.print(f"  Framework: {framework}")
    console.print(f"  Output: {output}\n")

    # Initialize skill
    build_skill = BuildSkill()

    # Create intent
    intent = Intent(
        type=IntentType.BUILD,
        raw_input=spec_file,
        confidence=0.9,
        parameters={
            "spec_file": spec_file,
            "framework": framework,
            "output": output,
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
        ("spec", "Execution Engine", "In Design", "Spec - Requirement to specification"),
        ("build", "Execution Engine", "In Design", "Build - Specification to code"),
        ("verify", "Execution Engine", "In Design", "Verify - Automated verification"),
        ("ship", "Execution Engine", "In Design", "Ship - Release & delivery"),
        ("review", "Quality Assurance", "Stable", "Review - Code review"),
        ("test", "Quality Assurance", "In Design", "Test - Intelligent testing"),
        ("audit", "Quality Assurance", "In Design", "Audit - Security audit"),
        ("gate", "Quality Assurance", "In Design", "Gate - Quality gate"),
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
    """View Helix status"""
    console.print(f"[bold]Helix Version:[/bold] {__version__}")
    console.print("[bold]Status:[/bold] Ready")
    console.print("")
    console.print("[bold]Supported Engines:[/bold]")
    console.print("  - Claude Code (In Development)")
    console.print("  - OpenClaw (Planned)")
    console.print("  - OpenCode (Planned)")
    console.print("  - Cursor (Planned)")
    console.print("  - GitHub Copilot CLI (Planned)")
    console.print("  - Gemini CLI (Planned)")


if __name__ == "__main__":
    main()
