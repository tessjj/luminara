import logging

import discord
from discord.ext import commands, bridge

from lib import checks
from lib.embeds.error import EconErrors
from modules.economy import leaderboard, blackjack, sell, slots, balance, stats, give, inventory, daily

logs = logging.getLogger('Racu.Core')


class Economy(commands.Cog):

    def __init__(self, client):
        self.client = client

    @bridge.bridge_command(
        name="leaderboard",
        aliases=["lb", "xplb"],
        description="Are ya winning' son?",
        help="Shows the guild's level leaderboard by default. You can switch to currency and /daily leaderboard.",
        guild_only=True
    )
    @commands.check(checks.channel)
    @commands.cooldown(1, 180, commands.BucketType.user)
    async def leaderboard_command(self, ctx):
        return await leaderboard.cmd(ctx)

    @bridge.bridge_command(
        name="balance",
        aliases=["bal", "$"],
        description="See how much cash you have.",
        help="Shows your current Racu balance. The economy system is global, meaning your balance will be the same in "
             "all servers.",
        guild_only=True
    )
    @commands.check(checks.channel)
    async def balance_command(self, ctx):
        return await balance.cmd(ctx)

    @bridge.bridge_command(
        name="blackjack",
        aliases=["bj"],
        description="Start a game of blackjack.",
        help="Start a game of blackjack.",
        guild_only=True
    )
    @commands.check(checks.channel)
    async def blackjack_command(self, ctx, *, bet: int):
        return await blackjack.cmd(ctx, bet)

    @blackjack_command.error
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.respond(embed=EconErrors.missing_bet(ctx))
        elif isinstance(error, commands.BadArgument):
            await ctx.respond(embed=EconErrors.bad_bet_argument(ctx))
        else:
            raise error

    @bridge.bridge_command(
        name="daily",
        aliases=["timely"],
        description="Claim your daily cash!",
        help="Claim your daily reward! The daily reset is at 7 AM EST.",
        guild_only=True
    )
    @commands.check(checks.channel)
    async def daily(self, ctx):
        return await daily.cmd(ctx)

    @bridge.bridge_command(
        name="give",
        description="Give another user some currency.",
        help="Give another server member some cash.",
        guild_only=True
    )
    @commands.check(checks.channel)
    async def give(self, ctx, *, user: discord.Member, amount: int):
        return await give.cmd(ctx, user, amount)

    @bridge.bridge_command(
        name="inventory",
        aliases=["inv"],
        description="Display your inventory.",
        help="Display your inventory, this will also show your Racu badges if you have any.",
        guild_only=True
    )
    @commands.check(checks.channel)
    async def inventory(self, ctx):
        return await inventory.cmd(ctx)

    @commands.slash_command(
        name="sell",
        description="Sell items from your inventory.",
        guild_only=True
    )
    @commands.check(checks.channel)
    async def sell_command(self, ctx):
        return await sell.cmd(self, ctx)

    @bridge.bridge_command(
        name="slots",
        aliases=["slot"],
        descriptions="Spin the slots for a chance to win the jackpot!",
        help="Starts a slots game.",
        guild_only=True
    )
    @commands.check(checks.channel)
    async def slots_command(self, ctx, *, bet: int):
        return await slots.cmd(self, ctx, bet)

    @slots_command.error
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.respond(embed=EconErrors.missing_bet(ctx))
        elif isinstance(error, commands.BadArgument):
            await ctx.respond(embed=EconErrors.bad_bet_argument(ctx))
        else:
            raise error

    @commands.slash_command(
        name="stats",
        description="Display your stats (BETA)",
        guild_only=True
    )
    @commands.check(checks.channel)
    async def stats(self, ctx, *, game: discord.Option(choices=["BlackJack", "Slots"])):
        return await stats.cmd(self, ctx, game)


def setup(client):
    client.add_cog(Economy(client))
