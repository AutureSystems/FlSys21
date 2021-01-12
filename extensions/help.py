import discord
from discord.ext import commands


#under construcion


class help(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command
    async def help(self, ctx, page:int=1):
        await ctx.send("Sorry this command is under constructuion. Please check back later")


def setup(client):
    client.add_cog(help(client))
