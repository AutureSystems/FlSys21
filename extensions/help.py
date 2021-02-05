import discord
from discord.ext import commands
import math


class help(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def help(self, ctx, *, command=None):
        em = discord.Embed(tilte="Bot Help")
        if command is not None:
            for i in self.client.commands:
                if i == command:
                    em.description = f"{self.client.command_prefix}{i}"
                    if i.description is None:
                        desc = "No Description provided :<"
                    else:
                        desc = i.description
                    em.add_field(name="usage", value =f"{self.client.command_prefix}{i}{i.usage}")
                    em.add_field(name="description", value=desc)
                    break
                else:
                    em.description = f"No command with name {command} found"
        else:
            em.description = "Commands"
            for i in self.client.commands:
                if i.brief is None:
                    brief = "No short description provided"
                else:
                    brief = i.brief
                em.add_field(name=f"{self.client.command_prefix}{i}", value=brief)
        await ctx.send(embed=em)


def setup(client):
    client.add_cog(help(client))