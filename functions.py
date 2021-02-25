def qdel(number):
	with open('test.json', 'r') as f:
		queue = json.load(f)
		users = queue["users"]
		users.pop(number)

		with open('test.json', 'w') as f:
			json.dump(queue, f, indent=4)

async def fip(ctx):
	with open('test.json', 'r') as f:
		entry = json.load(f)
		users = entry["users"]
		topuser = users[0]
		print(topuser)
		host = await client.fetch_user(topuser["ID"])

		await ctx.send(f"First in place is {host.name}")

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

schedule.every(5).seconds.do(schedtest)

loop = asyncio.get_event_loop()
while True:
	loop.run_until_complete(schedule.run_pending())
	time.sleep(0.1)

@client.command()
async def insertDB(ctx, key, *, value):
	db[key] = value


@client.command()
async def getDB(ctx, key):
	msg = db[key]
	await ctx.send(msg)

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
	    "Test run sucessful! Actions completed: \n- defined first in the queue\n- checked FIP as pilot\n- if he confirmed: deleted the queue entry.")

#flight data
#pilot selection
#pilot assignemnt
  while db["qc"] == "false":
    with open('pilotqueues.json', 'r') as f:
      servers = json.load(f)
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
