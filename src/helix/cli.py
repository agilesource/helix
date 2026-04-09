"""
Helix CLI 入口
"""

import asyncio
import sys
from pathlib import Path

import click
from rich.console import Console
from rich.table import Table
from rich.syntax import Syntax
from rich.markdown import Markdown

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
    """Helix - AI 时代软件工程方法论新范式"""
    pass


@main.command()
@click.argument("input_text", required=False)
@click.option("--template", "-t", help="指定模板类型 (crud/api/algorithm/integration/ui/script/infrastructure)")
@click.option("--no-confirm", is_flag=True, help="跳过确认步骤")
@click.option("--output", "-o", type=click.Path(), help="输出文件路径")
def spec(input_text: str, template: str, no_confirm: bool, output: str):
    """规格说明技能 - 将需求转化为结构化规格说明书

    用法:
        helix spec "我想做一个用户登录功能"
        helix spec "创建一个用户管理API" --template api
        helix spec  # 交互模式
    """
    if not input_text:
        console.print("[yellow]进入交互模式...[/yellow]")
        input_text = click.prompt("请描述你想要的功能", type=str)

    console.print(f"\n[bold blue]⚡ Helix Spec[/bold blue] - 正在处理需求")
    console.print(f"  输入: {input_text}\n")

    # 初始化技能
    skill_config = SkillConfig(auto_confirm=no_confirm)
    spec_skill = SpecSkill(skill_config)

    # 创建意图
    intent = Intent(
        type=IntentType.SPEC,
        raw_input=input_text,
        confidence=0.9
    )

    # 执行技能
    try:
        result = asyncio.run(spec_skill.execute(intent, None))

        if result.success:
            console.print("[bold green]✓[/bold green] 规格说明书已生成\n")

            # 显示生成的 Spec
            spec_content = result.data.get("spec_content", "")
            console.print(Panel(spec_content, title="生成的规格说明书", border_style="blue"))

            # 需求类型
            req_type = result.data.get("requirement_type", "general")
            console.print(f"[dim]需求类型: {req_type}[/dim]\n")

            # 保存到文件
            if output:
                Path(output).write_text(spec_content)
                console.print(f"[green]✓[/green] 已保存到: {output}")
            elif not no_confirm:
                # 确认保存
                save = click.confirm("是否保存到文件?", default=True)
                if save:
                    filename = f"SPEC.md"
                    Path(filename).write_text(spec_content)
                    console.print(f"[green]✓[/green] 已保存到: {filename}")
        else:
            console.print(f"[bold red]✗[/bold red] {result.message}")

    except Exception as e:
        console.print(f"[bold red]✗[/bold red] 执行出错: {e}")
        sys.exit(1)


@main.command()
def templates():
    """列出所有可用模板"""
    table = Table(title="可用规格说明书模板")
    table.add_column("模板名称", style="cyan")
    table.add_column("适用场景", style="magenta")
    table.add_column("描述")

    templates = [
        ("crud", "CRUD 操作", "数据增删改查管理"),
        ("api", "API 服务", "REST/GraphQL 接口"),
        ("algorithm", "算法实现", "排序、搜索、推荐等算法"),
        ("integration", "第三方集成", "对接外部服务"),
        ("ui", "页面/组件", "前端页面和组件"),
        ("script", "脚本工具", "命令行工具和脚本"),
        ("infrastructure", "基础设施", "部署、CI/CD 等"),
    ]

    for name, scenario, desc in templates:
        table.add_row(name, scenario, desc)

    console.print(table)


@main.command()
@click.argument("spec_file", type=click.Path(exists=True))
@click.option("--framework", "-f", default="fastapi", help="框架类型 (fastapi/django/express)")
@click.option("--output", "-o", default=".", help="输出目录")
@click.option("--dry-run", is_flag=True, help="仅预览，不生成文件")
def build(spec_file: str, framework: str, output: str, dry_run: bool):
    """代码骨架生成 - 根据规格说明书生成代码

    用法:
        helix build SPEC.md
        helix build SPEC.md --framework fastapi
        helix build SPEC.md -o ./src
    """
    console.print(f"\n[bold blue]⚡ Helix Build[/bold blue] - 正在生成代码骨架")
    console.print(f"  规格: {spec_file}")
    console.print(f"  框架: {framework}")
    console.print(f"  输出: {output}\n")

    # 初始化技能
    build_skill = BuildSkill()

    # 创建意图
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

    # 执行技能
    try:
        result = asyncio.run(build_skill.execute(intent, None))

        if result.success:
            console.print("[bold green]✓[/bold green] 代码骨架已生成\n")

            # 显示生成的文件
            files = result.data.get("files", [])
            table = Table(title="生成的文件")
            table.add_column("文件", style="cyan")
            table.add_column("路径", style="magenta")

            for f in files:
                table.add_row(f.split('/')[-1], f)

            console.print(table)

            console.print(f"\n[dim]使用说明:[/dim]")
            console.print(f"  1. 安装依赖: pip install -r requirements.txt")
            console.print(f"  2. 启动服务: python main.py")
            console.print(f"  3. 运行测试: pytest")
        else:
            console.print(f"[bold red]✗[/bold red] {result.message}")

    except Exception as e:
        console.print(f"[bold red]✗[/bold red] 执行出错: {e}")
        import traceback
        console.print(f"[dim]{traceback.format_exc()}[/dim]")
        sys.exit(1)


@main.command()
@click.argument("path", default=".", required=False)
@click.option("--level", "-l", default="full",
              type=click.Choice(["static", "test", "acceptance", "full"]),
              help="验证层级")
def verify(path: str, level: str):
    """自动化验证 - 运行静态检查、单元测试、验收测试

    用法:
        helix verify
        helix verify ./src
        helix verify --level static
    """
    console.print(f"\n[bold blue]⚡ Helix Verify[/bold blue] - 正在验证")
    console.print(f"  路径: {path}")
    console.print(f"  层级: {level}\n")

    # 初始化技能
    verify_skill = VerifySkill()

    # 创建意图
    intent = Intent(
        type=IntentType.VERIFY,
        raw_input=path,
        confidence=0.9,
        parameters={
            "path": path,
            "level": level,
        }
    )

    # 执行技能
    try:
        result = asyncio.run(verify_skill.execute(intent, None))

        if result.success or "PARTIAL" in result.message or "partial" in result.message.lower():
            console.print(result.message)
        else:
            console.print(f"[bold red]✗[/bold red] 验证失败")
            console.print(result.message)

    except Exception as e:
        console.print(f"[bold red]✗[/bold red] 执行出错: {e}")
        sys.exit(1)


@main.command()
@click.argument("input_text")
def classify(input_text: str):
    """测试需求类型识别"""
    spec_skill = SpecSkill()
    req_type = spec_skill._classify_requirement(input_text)
    entities = spec_skill._extract_entities(input_text)

    console.print(f"\n[bold]输入:[/bold] {input_text}\n")
    console.print(f"[bold]识别类型:[/bold] {req_type.value}")
    console.print(f"[bold]提取实体:[/bold]")
    console.print(f"  领域: {entities.domain or '(未识别)'}")
    console.print(f"  动作: {entities.action or '(未识别)'}")
    console.print(f"  集成: {entities.integrations or '无'}")


@main.command()
def list_skills():
    """列出所有可用技能"""
    table = Table(title="Helix 可用技能")
    table.add_column("名称", style="cyan")
    table.add_column("分类", style="magenta")
    table.add_column("状态", style="green")
    table.add_column("描述")

    skills = [
        ("spec", "执行引擎", "设计中", "规格说明 - 需求转规格"),
        ("build", "执行引擎", "设计中", "智能构建 - 规格转代码"),
        ("verify", "执行引擎", "设计中", "自动化验证"),
        ("ship", "执行引擎", "设计中", "发布交付"),
        ("review", "质量保障", "稳定", "代码审查"),
        ("test", "质量保障", "设计中", "智能测试"),
        ("audit", "质量保障", "设计中", "安全审计"),
        ("gate", "质量保障", "设计中", "质量门禁"),
        ("browse", "基础设施", "稳定", "浏览器控制"),
        ("design", "基础设施", "稳定", "设计生成"),
        ("learn", "基础设施", "稳定", "持续学习"),
        ("checkpoint", "基础设施", "稳定", "状态保存"),
    ]

    for name, category, status, desc in skills:
        table.add_row(f"/{name}", category, status, desc)

    console.print(table)


@main.command()
def status():
    """查看 Helix 状态"""
    console.print(f"[bold]Helix 版本:[/bold] {__version__}")
    console.print("[bold]状态:[/bold] 就绪")
    console.print("")
    console.print("[bold]支持引擎:[/bold]")
    console.print("  - Claude Code (开发中)")
    console.print("  - OpenClaw (计划中)")
    console.print("  - OpenCode (计划中)")
    console.print("  - Cursor (计划中)")
    console.print("  - GitHub Copilot CLI (计划中)")
    console.print("  - Gemini CLI (计划中)")


# 添加 Panel 用于显示
from rich.panel import Panel

if __name__ == "__main__":
    main()
