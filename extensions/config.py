import discord
import aiosqlite
from discord.ext import commands
import json
import time

color = 0x131581
client = commands

class config(commands.Cog):
  def __init__(self, client):
    self.client = client

  @commands.command()
  @commands.has_permissions(administrator=True)
  async def setup(self, ctx):
    with open('servers.json', 'r') as f:
        servers = json.load(f)
    for current_server in servers['servers']:
        if current_server['server_ID'] == ctx.guild.id:
            await ctx.send("This server is already setup! Use fl!help to get info on how to change individual things.")
            break
    else:
        qlist = [
        "What is your flight announcements channel ID?",
        "What is your timezone?",
        
    ]

        alist = []

        channel = ctx.channel

        def check(m):
            return m.content is not None and m.channel == channel and not m.author.bot

        for q in qlist:
            await ctx.send(q)
            msg = await self.client.wait_for('message', check=check)
            alist.append(msg.content)
        
        servers['servers'].append({
            "server_ID": ctx.guild.id,
            "channel_ID": int(alist[0]),
            "timezone": alist[1],
            "fleet": [],
        })
        await ctx.send(f"Initial setup done! Review your servers configuration using fl!serverconfig. Next up please use fl!fleet to enter your fleet.")
    with open('servers.json', 'w') as f:
        json.dump(servers, f, indent=4)

  @commands.command()
  @commands.has_permissions(administrator=True)
  async def fleet(self, ctx):
    def check(m):
        return m.content is not None and not m.author.bot and m.author == ctx.author
    with open('servers.json', 'r') as f:
        servers = json.load(f)
    for current_server in servers['servers']:
      if current_server['server_ID'] == ctx.guild.id:
        fleetsetup = discord.Embed(title="Fleet Setup", description="Welcome to the fleet setup! Please enter your fleet *one by one* and only when you're asked to do as it won't be used correctly otherwise. We will now start with your fleet setup.")
        await ctx.send(embed=fleetsetup)
        submit_wait = True
        fleetlist = []
        while submit_wait:
          await ctx.send("Enter a plane or type 'done' to submit your fleet!")
          msg = await self.client.wait_for('message', check=check)
          fleetlist.append(msg.content)
          time.sleep(0.5)
          if "done" in msg.content.lower():
            submit_wait = False
            current_server["fleet"] = fleetlist
            with open('servers.json', 'w') as f:
              json.dump(servers, f, indent=4)
            await ctx.send("Fleet submitted! Congratulations!")

  

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