import discord
from discord.ext import commands
import math


class help(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def help(self, ctx, *, cog=None):
        em = discord.Embed(title="Bot help")
        if cog is not None:
            try:
                cogi = self.client.get_cog(str(cog).lower())
                cmds = cogi.get_commands()
                for cmd in cmds:
                    if cmd.description is None:
                        desc = "No Description provided"
                    else:
                        desc = cmd.description
                    em.add_field(name=cmd, value=desc, inline = True)
            except:
                tlist = []
                for i in self.client.commands:
                    tlist.append(i)
                for b in tlist:
                    if b.name == cog:
                        if b.description is None:
                            desc = "No Description provided"
                        else:
                            desc = b.description
                        em.add_field(name=b.name, value=f"{desc}\nUsage:\n{self.client.command_prefix}{b.name} {b.usage}")
                        break
                    em.description = f"No command or category named {cog} found"
        else:
            for cogp in self.client.cogs:
                cogm = self.client.get_cog(cogp)
                if cogm.description is None:
                    desc = "No Description provided"
                else:
                    desc = cogm.description
                em.add_field(name=cogm.qualified_name, value=desc, inline = False)
                em.description = "Categories:"
        em.set_footer(text="() means optional and {} means required")
        await ctx.send(embed=em)


def setup(client):
    client.add_cog(help(client))