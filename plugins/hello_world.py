"""
Example Skill Plugin - Hello World

Demonstrates how to create a skill plugin for Helix
"""

from helix.plugins.base import (
    Plugin, PluginMetadata, PluginConfig, PluginType,
    SkillPlugin, PluginResult
)
from helix.skills.base import Skill, SkillResult, SkillConfig


class HelloWorldSkill(Skill):
    """Simple hello world skill"""

    name = "hello"
    description = "Say hello to the user"
    category = None  # Will be set by plugin
    status = None    # Will be set by plugin

    examples = [
        "hello",
        "hello --name World",
    ]

    async def execute(self, intent, context):
        """Execute the skill"""
        name = intent.parameters.get("name", "World")
        message = f"Hello, {name}! Welcome to Project Helix."

        return SkillResult(
            success=True,
            message=message,
            data={"name": name},
        )


class HelloWorldPlugin(SkillPlugin):
    """
    Hello World Plugin

    A simple plugin that demonstrates the plugin system
    """

    metadata = PluginMetadata(
        name="helix-hello",
        version="0.1.0",
        description="A simple hello world skill plugin for Helix",
        author="Peter Cheng + Jarvis",
        author_email="petercheng@opensourcevalley.com",
        keywords=["example", "hello", "demo", "skill"],
        dependencies=[],
    )

    plugin_type = PluginType.SKILL

    def get_skill_class(self):
        """Return the skill class"""
        return HelloWorldSkill


# Register plugin instance
plugin = HelloWorldPlugin()
