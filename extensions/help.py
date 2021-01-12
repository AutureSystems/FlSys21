import discord
from discord.ext import commands


#under construcion


class help(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command
    async def help(self, ctx, page: int= 1):
        items_per_page = 10
        p_q = len(player.queue) + 1
        pages = math.ceil(p_q / items_per_page)
        start = (page - 1) * items_per_page
        end = start + items_per_page

        desc = ''
        for index, cmd in enumerate(self.client.commands[start:end], start=start):
            desc += f'fl!{cmd}\n'
        em = discord.Embed(title:"Commands", description=desc)
        await ctx.send(embed=em)


def setup(client):
    client.add_cog(help(client))
