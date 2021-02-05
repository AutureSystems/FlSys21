import discord
from discord.ext import commands
import json
import time
import asyncio
import aiosqlite
from colorama import Fore
from keep_alive import keep_alive
import aioschedule as schedule
import os
import difflib

intents = discord.Intents.default()
client = commands.Bot(
    command_prefix="fl!", help_command=None, intents=intents.all())


@client.event
async def on_ready():
  db = await aiosqlite.connect("main.sqlite")
  cursor = await db.cursor()
  cursor.execute(
	  """
	  CREATE TABLE IF NOT EXISTS flights(
		  channel_id TEXT,
		  guild_id TEXT,
		  flnumber TEXT,
		  departure TEXT,
		  destination TEXT,
		  arrival TEXT,
		  aircraft TEXT,
		  server TEXT,
		  gate TEXT,
		  time TEXT,
		  pilot,
		  fa,
		  fo,
		  gc,

	  )
	  """
  )
  for filename in os.listdir('./extensions'):
        if filename.endswith('.py'):
            client.load_extension(f'extensions.{filename[:-3]}')
            print(f'loading {filename}')
  print(Fore.GREEN + "[STATUS] Bot started")
  time.sleep(0.9)
  print(Fore.GREEN + "[STATUS] Aiosqlite database loaded")
  time.sleep(0.9)
  print(Fore.YELLOW + "[WARNING] If you encounter a problem please terminate the process")
  time.sleep(5)
  print(Fore.RESET + "[DONE] Bot succesfully executed")

@client.event
async def on_command_error(ctx, error):
	if isinstance(error, commands.CommandNotFound):
		emv = "I Dont know that command!"
		cmd = ctx.message.content.split()[0].replace(client.command_prefix, "")
		all_cmd = [i.name for i in client.commands]
		pos = difflib.get_close_matches(cmd, all_cmd, n=1)
		if pos:
			emv += f"\nMaybe you mean {client.command_prefix}{pos[0]}?"
	elif isinstance(error, commands.CommandOnCooldown):
		emv = "You are on cooldown, try again in {} seconds".format(error.retry_after)
	elif isinstance(error, commands.MessageNotFound):
		emv = "I can't find {} message!".format(error.argument)
	elif isinstance(error, commands.MemberNotFound) or isinstance(error, commands.UserNotFound):
		emv = "I can't find {} user!".format(error.argument)
	elif isinstance(error, commands.ChannelNotFound):
		emv = "I can't find {} channel!".format(error.argument)
	elif isinstance(error, commands.ChannelNotReadable):
		emv = "I don't have permission to read message in {} channel!".format(error.argument)
	elif isinstance(error, commands.RoleNotFound):
		emv = "I can't find {} role!".format(error.argument)
	elif isinstance(error, commands.DisabledCommand):
		emv = "That command is disabled!"
	elif isinstance(error, commands.NoPrivateMessage):
		emv = "You can't run this command on private message or DM!"
	elif isinstance(error, commands.PrivateMessageOnly):
		emv = "You can only run in private message or DM!"
	elif isinstance(error, commands.MissingRequiredArgument):
		emv = "Im missing {} parameter to run this command properly".format(error.param)
	elif isinstance(error, commands.NotOwner):
		emv = "Sorry but this command is for owner only!"
	elif isinstance(error, commands.EmojiNotFound):
		emv = "I can't find {} emoji!".format(error.argument)
	elif isinstance(error, commands.MissingPermissions):
		emv = "You missing {} permission to run that command!".format(error.missing_perms)
	elif isinstance(error, commands.BotMissingPermissions):
		emv = "Im missing {} permission to execute that command!".format(error.missing_perms)
	elif isinstance(error, commands.MissingRole):
		emv = "You missing {} role to run this command!".format(error.missing_role)
	elif isinstance(error, commands.BotMissingRole):
		emv = "Im need {} role to run this command!".format(error.missing_role)
	elif isinstance(error, commands.MissingAnyRole):
		emv = "You missing {} roles to run this command!".format(error.missing_roles)
	elif isinstance(error, commands.BotMissingAnyRole):
		emv = "Im need {} role to run this command!".format(error.missing_roles)
	else:
		emv = f"An unexpected error has occured! The error:\n{error}"
	em = discord.Embed(titlle="An error has occured!", description=emv)
	em.set_footer(text="Is this a bug? Let us know!")
	await ctx.send(embed=em)
	raise error

async def flight():
  db = await aiosqlite.connect("main.sqlite")
  for i in client.guilds:
	  ccursor = await db.execute(f"SELECT channel_id FROM flights WHERE guild_id = {i.id}")
	  ncursor = await db.execute(f"SELECT flnumber FROM flights WHERE guild_id = {i.id}")
	  dcursor = await db.execute(f"SELECT departure FROM flights WHERE guild_id = {i.id}")
	  acursor = await db.execute(f"SELECT destination FROM flights WHERE guild_id = {i.id}")
	  flighttime = await db.execute(f"SELECT time FROM flights WHERE guild_id = {i.id}")
	  aircrafttype = await db.execute(f"SELECT aircraft FROM flights WHERE guild_id = {i.id}")
	  chan = await ccursor.fetchone()
	  flnumber = await ncursor.fetchone()
	  dptr = await dcursor.fetchone()
	  arrvl = await acursor.fetchone()
	  fltime = await flighttime.fetchone()
	  aircraft = await aircrafttype.fetchone()

  channel = client.get_channel(int(chan[0]))
  flight = discord.Embed(
  title=
  f"<:BA1:761894114484420609><:BA2:761894114785755176><:BA3:761894115087482930> British Airways Flight {flnumber}",
  description=
  f"Departure Airport: {dptr} \nDestination Airport: {arrvl} \n\nTodays Aircraft: {aircraft} \nTime Of Flight Is {fltime} \nTimezone is GMT \n\nFirst Class: <:FirstClass:757170500454580224>\nBusiness Class: <:BusinessClass:757171994121732157>\nEconomy Class: <:GreatBritain:714843928431558676>\n\n Listing of passengers ends **30 minutes before flight**!\n-------------\n",
  colour=0xff0000)
  flight.set_footer(text=f"To fly, to serve!")
  msg = await channel.send(f"<@&717681307483635722>", embed=flight)

  await msg.add_reaction(emoji="<:FirstClass:757170500454580224>")
  await msg.add_reaction(emoji="<:BusinessClass:757171994121732157>")
  await msg.add_reaction(emoji="<:GreatBritain:714843928431558676>")


@client.command()
@commands.has_permissions(manage_messages=True)
async def boarding(ctx):
   db = await aiosqlite.connect("main.sqlite")
   for i in client.guilds:
	  	value = await db.execute(f"SELECT server FROM flights WHERE guild_id = {i.id}")
	  	gate = await db.execute(f"SELECT gate FROM flights WHERE guild_id = {i.id}")
	  	dep = await db.execute(f"SELECT departure FROM flights WHERE guild_id = {i.id}")
	  	fo = await db.execute(f"SELECT fo FROM flights WHERE guild_id = {i.id}")
	  	pilots = await db.execute(f"SELECT pilot FROM flights WHERE guild_id = {i.id}")
	  	flightnumb = await db.execute(f"SELECT flnumber FROM flights WHERE guild_id = {i.id}")
	  	gate = await gate.fetchone()
	  	flnumber = await flightnumb.fetchone()
	  	airport = await dep.fetchone()
	  	pilot = await pilots.fetchone()
	  	f_o = await fo.fetchone()
	  	server = await value.fetchone()
   boarding = discord.Embed(
	    title=
	    f"<:BA1:761894114484420609><:BA2:761894114785755176><:BA3:761894115087482930> British Airways Flight {flnumber}",
	    description=
	    f"Flight {flnumber} is now boarding at:\n \n- Airport: {airport} \n- Gate: {gate} \n-------------------\n {value} \n-------------------\nPlease join VC for a better experience, \nthere's no need for a mic!\n-------------------\n- todays pilot: {pilot}\n- todays first officer: {f_o}",
	    colour=0xff0000)
   boarding.set_footer(text="To fly, to serve!")
   boarding.set_thumbnail(
	    url=
	    "http://logok.org/wp-content/uploads/2014/04/British-Airways-logo-ribbon-logo-880x660.png"
	)
   await ctx.send(f"<@&717681307483635722>", embed=boarding)


def qdel(number):
	with open('test.json', 'r') as f:
		queue = json.load(f)
		users = queue["users"]
		users.pop(number)

		with open('test.json', 'w') as f:
			json.dump(queue, f, indent=4)


def pqdel(number):
	with open('pq.json', 'r') as f:
		queue = json.load(f)
		users = queue["users"]
		users.pop(number)

		with open('pq.json', 'w') as f:
			json.dump(queue, f, indent=4)


def foqdel(number):
	with open('foq.json', 'r') as f:
		queue = json.load(f)
		users = queue["users"]
		users.pop(number)

		with open('foq.json', 'w') as f:
			json.dump(queue, f, indent=4)


def faqdel(number):
	with open('faq.json', 'r') as f:
		queue = json.load(f)
		users = queue["users"]
		users.pop(number)

		with open('faq.json', 'w') as f:
			json.dump(queue, f, indent=4)


async def fip(ctx):
	with open('test.json', 'r') as f:
		entry = json.load(f)
		users = entry["users"]
		topuser = users[0]
		print(topuser)
		host = await client.fetch_user(topuser["ID"])

		await ctx.send(f"First in place is {host.name}")


async def check(ctx, user: discord.User, role):

  channel = await user.create_dm()
  fltime = db["fltime"]
  flnumber = db["flnumber"]
  if role.lower() == "pilot":
    check = discord.Embed(
        title=f"Flight at {fltime}",
        description=
        f"You've been selected to be todays pilot on flight {flnumber}. \n\nIf you are available at {fltime} GMT please use the tick reaction below in the next **5 minutes**, if not please choose the cross!",
        color=0xff0000)
    check.set_author(
        name="BA Staff Team",
        icon_url=
        "http://logok.org/wp-content/uploads/2014/04/British-Airways-logo-ribbon-logo.png"
    )
  elif role.lower() == "f/o":
    check = discord.Embed(
        title=f"Flight at {fltime}",
        description=
        f"You've been selected to be todays first officer on flight {flnumber}. \n\nIf you are available at {fltime} please use the tick reaction below in the next **20 minutes**, if not please choose the cross!",
        color=0xff0000)
    check.set_author(
        name="BA Staff Team",
        icon_url=
        "http://logok.org/wp-content/uploads/2014/04/British-Airways-logo-ribbon-logo.png"
    )
  elif role.lower() == "f/a":
    check = discord.Embed(
        title=f"Flight at {fltime}",
        description=
        f"You've been selected to be todays flight attendant on flight {flnumber}. \n\nIf you are available at {fltime} please use the tick reaction below in the next **20 minutes**, if not please choose the cross!",
        color=0xff0000)
    check.set_author(
        name="BA Staff Team",
        icon_url=
        "http://logok.org/wp-content/uploads/2014/04/British-Airways-logo-ribbon-logo.png"
    )

  msg = await channel.send(embed=check)
  await ctx.send(f"Waiting for {role} to confirm")
  await msg.add_reaction(str('✅'))
  await msg.add_reaction(str('❌'))

  def uc(reaction, user2):
    return user2 == user and (str(reaction.emoji) == '✅' or str(reaction.emoji) == '❌')

  try:
    reaction, user2 = await client.wait_for(
        'reaction_add', timeout=10.0, check=uc)
  except asyncio.TimeoutError:
    await channel.send(
        "You didn't confirm in the given 5 minutes! You were put back into the queue."
    )
    await ctx.send(
        f"No confirmation received by the {role} in time. Trying the next one!"
    )
  else:
    if reaction.emoji == str('✅'):
      await channel.send(
          f"Thanks for confirming! See you in the plane at {fltime}. Your Queue entry has been deleted, you can re-enter the queue after the flight."
      )
      await ctx.send(
          f"<a:BAcheck:758094859491082373> The {role} confirmed that he'll available! \n\nI have assigned {user} as {role} for todays flight! If you want to change this later use either \n-b!pilot [user] \n-b!f_o [user] \n-b!cabincrew [user]\ndepending on the role you'd like to change."
      )
      if role.lower() == "pilot":
        db["pilot"] = str(user)
        db["qc"] = "true"
      elif role.lower() == "f/o":
        db["fo"] = str(user)
        db["qc"] = "true"
      elif role.lower() == "f/a":
        db["cabincrew"] = str(user)
        db["qc"] = "true"
    elif reaction.emoji == str('❌'):
      await channel.send(
          f"Thanks for replying! You were put back into the queue!")
      await ctx.send(
          f"❌ The {role} {user} won't be available and declined. Trying the next one."
      )
    else:
      print("NOpeIStupidanddudmmm")


@client.command(pass_context=True)
async def testqueue(ctx):
	with open('test.json', 'r') as f:
		entry = json.load(f)
		user = ctx.author.id
	for current_user in entry['users']:
		if current_user['ID'] == user:
			await ctx.send(
			    f"Hello {ctx.author.name}! You have already entered the queue")
			break
	else:
		entry['users'].append({
		    'ID': user,
		})
		with open('test.json', 'w') as f:
			json.dump(entry, f, indent=4)
		await ctx.send(f"You entered the queue!")


@client.command(pass_context=True)
async def insertqueue(ctx, user: discord.User):
	with open('test.json', 'r') as f:
		entry = json.load(f)
	for current_user in entry['users']:
		if current_user['ID'] == user.id:
			await ctx.send(
			    f"Hello {ctx.author.name}! You have already entered the queue")
			break
	else:
		entry['users'].append({
		    'ID': user.id,
		})
		with open('test.json', 'w') as f:
			json.dump(entry, f, indent=4)
		await ctx.send(f"You inserted {user.name} into the queue!")


@client.command(pass_context=True)
async def testqread(ctx):
	with open('test.json', 'r') as f:
		entry = json.load(f)
		users = entry["users"]
		topuser = users[0]
		print(topuser)
		host = await client.fetch_user(topuser["ID"])

		await ctx.send(f"First in place is {host.name}")


@client.command(pass_context=True)
async def testqdel(ctx):
	with open('test.json', 'r') as f:
		queue = json.load(f)
		users = queue["users"]
		users.pop(0)

		with open('test.json', 'w') as f:
			json.dump(queue, f, indent=4)


@client.command()
#@commands.has_any_role(785783017104605194, 739429658541424671, 707777754409467906, 739442933215789056, 737944971201740801)
async def joinqueue(ctx, role):
	entered = None
	if role.lower() == "pilot":
		qr = "pilot"
		with open('pq.json', 'r') as f:
			entry = json.load(f)
			user = ctx.author.id
		for current_user in entry['users']:
			if current_user['ID'] == user:
				await ctx.send(
				    f"Hello {ctx.author.name}! You have already entered the queue"
				)
				entered = True
				break
		if entered == None:
			entry['users'].append({
			    'ID': user,
			})
			with open('pq.json', 'w') as f:
				json.dump(entry, f, indent=4)
			msg = await ctx.send(
			    f"<a:BAcheck:758094859491082373> Action succesful! You joined the {qr} queue!"
			)
	elif role.lower() == "f/o":
		qr = "first officer"
		with open('foq.json', 'r') as f:
			entry = json.load(f)
			user = ctx.author.id
		for current_user in entry['users']:
			if current_user['ID'] == user:
				await ctx.send(
				    f"Hello {ctx.author.name}! You have already entered the queue"
				)
				entered = True
				break
		if entered == None:
			entry['users'].append({
			    'ID': user,
			})
			with open('foq.json', 'w') as f:
				json.dump(entry, f, indent=4)
			msg = await ctx.send(
			    f"<a:BAcheck:758094859491082373> Action succesful! You joined the {qr} queue!"
			)
	elif role.lower() == "f/a":
		qr = "flight attendant"
		with open('faq.json', 'r') as f:
			entry = json.load(f)
			user = ctx.author.id
		for current_user in entry['users']:
			if current_user['ID'] == user:
				await ctx.send(
				    f"Hello {ctx.author.name}! You have already entered the queue"
				)
				entered = True
				break
		if entered == None:
			entry['users'].append({
			    'ID': user,
			})
			with open('faq.json', 'w') as f:
				json.dump(entry, f, indent=4)
			msg = await ctx.send(
			    f"<a:BAcheck:758094859491082373> Action succesful! You joined the {qr} queue!"
			)

	time.sleep(3)
	await ctx.message.delete()
	await msg.delete()


@client.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def flights(ctx, status):
	if status.lower() == "enable":
		db["flstatus"] = "enabled"
		await ctx.send("Automated flights enabled!")
	elif status.lower() == "disable":
		db["flstatus"] = "disabled"
		await ctx.send("Automated flights disabled!")
	else:
		await ctx.send("Please state a valid status! (enable/disable)")



@client.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def testrun(ctx):
	db["qc"] = "false"
	c = 0
	role = "pilot"
	await ctx.send("Starting Demo")
	time.sleep(2)
	await ctx.send("Test queue checked, starting assignment")
	await fip(ctx)
	while db["qc"] == "false":
		with open('test.json', 'r') as f:
			entry = json.load(f)
			users = entry["users"]
			topuser = users[c]
			c = c + 1
			host = await client.fetch_user(topuser["ID"])
		await check(ctx, host, role)
	time.sleep(1)
	if db["qc"] == "true":
		number = c - 1
		qdel(number)
	else:
		await ctx.send(
		    f"{role} couldn't be assigned as there were no more queue entries")
	await ctx.send(
	    "Test run sucessful! Actions completed: \n- defined first in the queue\n- checked FIP as pilot\n- if he confirmed: deleted the queue entry."
	)


async def FlSys21(ctx):
  db["qc"] = "false"
  c = 0
  await ctx.send("programm started")
  time.sleep(2)
  await ctx.send("Checking Queues and assigning users")
  #pilot assignemnt
  while db["qc"] == "false":
    with open('pq.json', 'r') as f:
      entry = json.load(f)
      users = entry["users"]
      topuser = users[c]
      c = c + 1
      host = await client.fetch_user(topuser["ID"])
    await check(ctx, host, role="pilot")
  time.sleep(1)
  if db["qc"] == "true":
    number = c - 1
    pqdel(number)
  db["qc"] = "false"
  c = 0
  #F/O assignment
  while db["qc"] == "false":
    with open('foq.json', 'r') as f:
      entry = json.load(f)
      users = entry["users"]
      topuser = users[c]
      c = c + 1
      host = await client.fetch_user(topuser["ID"])
    await check(ctx, host, role="f/o")
  time.sleep(1)
  if db["qc"] == "true":
    number = c - 1
    foqdel(number)
  db["qc"] = "false"
  c = 0
  #F/A assignment
  while db["qc"] == "false":
    with open('faq.json', 'r') as f:
      entry = json.load(f)
      users = entry["users"]
      topuser = users[c]
      c = c + 1
      host = await client.fetch_user(topuser["ID"])
    await check(ctx, host, role="f/a")
  time.sleep(1)
  if db["qc"] == "true":
    number = c - 1
    foqdel(number)
  db["qc"] = "false"
  c = 0
  #flight announcement
  await flight()


async def OpenGate():
  #OpenGate function for scheduling.
  await boarding()


@client.command()
@commands.has_permissions(administrator=True)
async def starttest(ctx):
  await FlSys21(ctx)

@client.command()
async def insertDB(ctx, key, *, value):
	db[key] = value


@client.command()
async def getDB(ctx, key):
	msg = db[key]
	await ctx.send(msg)


#schedule.every(5).seconds.do(schedtest)

#loop = asyncio.get_event_loop()
#while True:
	#loop.run_until_complete(schedule.run_pending())
	#time.sleep(0.1)

keep_alive()
client.run(os.getenv("DISCORD_TOKEN"))
