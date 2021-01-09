import discord
import aiosqlite
from discord.ext import commands

color = 0x131581

class config(commands.Cog):
  def __init__(self, client):
    self.client = client


  @commands.command()
  @commands.has_permissions(manage_channels=True)
  async def flightchannel(self, ctx, channel : discord.TextChannel=None):
    db = await aiosqlite.connect("main.sqlite")
    cursor = await db.cursor()
    cursor.execute(f"SELECT channel_id FROM flights WHERE guild_id = {ctx.guild.id}")
    result = cursor.fetchone()
    if channel == None:
        em = discord.Embed(color=color)
        em.description = "fl!flightchannel {channel}"
        em.title = "Flightchannel command"
        return await ctx.send(embed=em)
    elif result == None:
        sql = ("INSERT INTO flights(guild_id, channel) VALUES(?,?)")
        val = (ctx.guild.id, channel)
        em = discord.Embed(color=discord.Color.green)
        em.description = f"Succesfully set the flight channel to {channel.mention}"
        await ctx.send(embed=em)
    elif result is not None:
        sql = ("UPDATE flights SET channel = ? WHERE guild_id = ?")
        val = (channel, ctx.guild.id)
        em = discord.Embed(color=discord.Color.green)
        em.description = f"Succesfully updated the flight channel to {channel.mention}"
        await ctx.send(embed=em)
    await cursor.execute(sql, val)
    await db.commit()
    await cursor.close()
    await db.close()
    





def setup(client):
    client.add_cog(config(client))
    return