import discord

import lib.formatter
from config.parser import JsonCache

resources = JsonCache.read_json("art")
exclaim_icon = resources["icons"]["exclaim"]
boost_icon = resources["icons"]["boost"]


class Boost:
    @staticmethod
    def message(member, template=None, image_url=None):
        embed = discord.Embed(
            color=discord.Color.nitro_pink(),
            title="New Booster",
            description=f"Thanks for boosting, **{member.name}**!!"
        )

        if template:
            # REPLACE
            embed.description = lib.formatter.template(template, member.name)

        embed.set_author(name=member.name, icon_url=member.display_avatar)
        embed.set_image(url=image_url if image_url else boost_icon)
        embed.set_footer(text=f"Total server boosts: {member.guild.premium_subscription_count}",
                         icon_url=exclaim_icon)

        return embed
