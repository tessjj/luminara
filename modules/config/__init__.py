import discord
from discord.commands import SlashCommandGroup
from discord.ext import bridge, commands

from config.parser import JsonCache
from modules.config import (
    c_show,
    c_birthday,
    c_greet,
    c_boost,
    c_level,
    set_prefix,
    xp_reward,
)

strings = JsonCache.read_json("strings")


class Config(commands.Cog):
    def __init__(self, client):
        self.client = client

    @bridge.bridge_command(
        name="setprefix",
        aliases=["sp"],
        description="Set Lumi's prefix.",
        help="Set the prefix for Lumi in this server. The maximum length of a prefix is 25.",
        guild_only=True,
    )
    @commands.guild_only()
    @commands.has_permissions(manage_channels=True)
    async def prefix_set_command(self, ctx, *, prefix: str):
        await set_prefix.set_cmd(ctx, prefix)

    @bridge.bridge_command(
        name="xprewards",
        aliases=["xpr"],
        description="Show your server's XP rewards list.",
        help="Read [the guide](https://wiki.wlinator.org/xprewards) before editing.",
        guild_only="True",
    )
    @commands.guild_only()
    @commands.has_permissions(manage_roles=True)
    async def xp_reward_command_show(self, ctx):
        await xp_reward.show(ctx)

    @bridge.bridge_command(
        name="addxpreward",
        aliases=["axpr"],
        description="Add a Lumi XP reward.",
        help="Add a Lumi XP reward. Read [the guide](https://wiki.wlinator.org/xprewards) before editing.",
        guild_only="True",
    )
    @commands.guild_only()
    @commands.has_permissions(manage_roles=True)
    async def xp_reward_command_add(
        self,
        ctx,
        level: int,
        role: discord.Role,
        persistent: bool = False,
    ):
        await xp_reward.add_reward(ctx, level, role.id, persistent)

    @bridge.bridge_command(
        name="removexpreward",
        aliases=["rxpr"],
        description="Remove a Lumi XP reward.",
        help="Remove a Lumi XP reward. Read [the guide](https://wiki.wlinator.org/xprewards) before editing.",
        guild_only="True",
    )
    @commands.guild_only()
    @commands.has_permissions(manage_roles=True)
    async def xp_reward_command_remove(self, ctx, level: int):
        await xp_reward.remove_reward(ctx, level)

    """
    CONFIG GROUPS
    The 'config' group consists of many different configuration types, each being guild-specific and guild-only.
    All commands in this group are exclusively available as slash-commands.
    Only members with "manage guild" permissions can access commands in this group.
    
    - Birthdays
    - Welcome
    - Boosts
    - Levels
    - Modlog channel
    - XP rewards
    - Permissions preset (coming soon)
    
    Running '/config show' will show a list of all available configuration types.
    """
    config = SlashCommandGroup(
        "config",
        "server config commands.",
        guild_only=True,
        default_member_permissions=discord.Permissions(manage_guild=True),
    )

    @config.command(name="show")
    async def config_command(self, ctx):
        await c_show.cmd(ctx)

    birthday_config = config.create_subgroup(name="birthdays")

    @config.command(name="birthdays")
    async def config_birthdays_channel(self, ctx, channel: discord.TextChannel):
        await c_birthday.set_birthday_channel(ctx, channel)

    @birthday_config.command(name="disable")
    async def config_birthdays_disable(self, ctx):
        await c_birthday.disable_birthday_module(ctx)

    welcome_config = config.create_subgroup(name="greetings")

    @welcome_config.command(name="channel")
    async def config_welcome_channel(self, ctx, channel: discord.TextChannel):
        await c_greet.set_welcome_channel(ctx, channel)

    @welcome_config.command(name="disable")
    async def config_welcome_disable(self, ctx):
        await c_greet.disable_welcome_module(ctx)

    @welcome_config.command(name="template")
    @discord.commands.option(name="text", type=str, max_length=2000)
    async def config_welcome_template(self, ctx, text):
        await c_greet.set_welcome_template(ctx, text)

    boost_config = config.create_subgroup(name="boosts")

    @boost_config.command(name="channel")
    async def config_boosts_channel(self, ctx, channel: discord.TextChannel):
        await c_boost.set_boost_channel(ctx, channel)

    @boost_config.command(name="disable")
    async def config_boosts_disable(self, ctx):
        await c_boost.disable_boost_module(ctx)

    @boost_config.command(name="template")
    @discord.commands.option(name="text", type=str, max_length=2000)
    async def config_boosts_template(self, ctx, text):
        await c_boost.set_boost_template(ctx, text)

    @boost_config.command(name="image")
    @discord.commands.option(name="url", type=str, max_length=2000)
    async def config_boosts_image(self, ctx, url):
        await c_boost.set_boost_image(ctx, url)

    level_config = config.create_subgroup(name="levels")

    @level_config.command(name="channel")
    async def config_level_channel(self, ctx, channel: discord.TextChannel):
        await c_level.set_level_channel(ctx, channel)

    @level_config.command(name="currentchannel")
    async def config_level_samechannel(self, ctx):
        await c_level.set_level_current_channel(ctx)

    @level_config.command(name="disable")
    async def config_level_disable(self, ctx):
        await c_level.disable_level_module(ctx)

    @level_config.command(name="enable")
    async def config_level_enable(self, ctx):
        await c_level.enable_level_module(ctx)

    @level_config.command(name="type")
    @discord.commands.option(name="type", choices=["whimsical", "generic"])
    async def config_level_type(self, ctx, type):
        await c_level.set_level_type(ctx, type)

    @level_config.command(name="template")
    async def config_level_template(self, ctx, text: str):
        await c_level.set_level_template(ctx, text)


def setup(client):
    client.add_cog(Config(client))
