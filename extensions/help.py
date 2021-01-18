import discord
from discord.ext import commands
import math


class help(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def help(self, ctx, page: int= 1):
        items_per_page = 10
        p_q = len(self.client.commands) + 1
        pages = math.ceil(p_q / items_per_page)
        start = (page - 1) * items_per_page
        end = start + items_per_page
        c = [i for i in self.client.commands]

        desc = ''
        for index, cmd in enumerate(c[start:end], start=start):
            if cmd.description is None:
                desc = "No Description provided"
            else:
                desc = cmd.description
            desc += f'**fl!{cmd.name}**\n{desc}\n' 
        em = discord.Embed(title="Commands", description=f'{desc}', color=16515071)
        em.set_footer(text=f'Viewing page {page}/{pages}')
        await ctx.send(embed=em)


def setup(client):
    client.add_cog(help(client))