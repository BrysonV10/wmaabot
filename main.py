import os, discord, sys
from dotenv import load_dotenv
from discord.ext import commands
intents = discord.Intents.default()
intents.members = True
intents.reactions = True
bot = commands.Bot(command_prefix="w!", intents=intents)
client = discord.Client(intent=intents)
bot.remove_command("help")
@bot.event
async def on_ready():
  print("Connected to Discord as:")
  print(bot.user)
  game = discord.Game("Waiting for w!help")
  await bot.change_presence(status=discord.Status.online, activity=game)
servId = 695039585180319845
@bot.event
async def on_member_join(member):
  server = discord.utils.get(bot.guilds, id=servId)
  modChan = discord.utils.get(server.text_channels, name="moderator-only")
  memobj = discord.utils.get(server.members, id=member.id)
  restrictedAcc = discord.utils.get(server.roles, name="Outside-Aviation")
  await member.send("Hello, and welcome to the Official West Michigan Aviation Academy Discord Server! I'm the main bot in the WMAA server. I manage all roles and many systems within the server. I need a little bit of information from you to get started. Do you go to WMAA or are you WMAA staff? [Respond with 'yes' or 'no']")
  def checkMsg(m):
    return m.author == member and isinstance(m.channel, discord.channel.DMChannel)
  try:
    msg = await bot.wait_for('message', check=checkMsg, timeout=300)
  except Exception:
    await member.send("Due to bot limitations, I can only handle DM requests for a max of 5 minutes, and you timed it out. I've given you restricted access and DMed the moderators to handle your case.")
    await modChan.send(member.display_name + " timed out a DM strand. I've given them restricted access in the meantime.")
    await memobj.add_roles(restrictedAcc)
  if msg.content == "yes" or msg.content == "Yes":
    await member.send("Ok cool!")
    await member.send("What is a good nickname that the members in the server can use to talk to you?")
    nickname = await bot.wait_for("message", check=checkMsg)
    await memobj.edit(nick=nickname.content)
    await member.send("Your nickname has been set. Go to the #roles channel (https://discord.com/channels/695039585180319845/708150431729189005/746498758627295323) in the server to set up your roles! If I incorrectly set up your nickname, just use the `w!set_nick` command to set your nickname.")
  elif msg.content == "no" or msg.content == "No":
    await member.send("Ah ok. Currently this server is restricted to WMAA students and staff only. I can send a DM to the server owner who can let you in if you get access.")
    await memobj.add_roles(restrictedAcc)
    await modChan.send(member.display_name + " is requesting to join the server. I've given them restrictive priviliages in the meantime.")
  else:
    await member.send("I don't know what you mean. I'm going to assume you don't go to WMAA.")
    await memobj.add_roles(restrictedAcc)
@bot.event
async def on_raw_reaction_add(reaction):
  serv = discord.utils.get(bot.guilds, id=servId)
  mem = discord.utils.get(serv.members, id=reaction.user_id)
  chan = discord.utils.get(serv.channels, name="roles")
  msg = await chan.fetch_message(reaction.message_id)
  if mem == bot.user:
    return
  if msg:
    if msg.content[len(msg.content)-1] == "*":
      role = discord.utils.get(serv.roles, name=msg.content[:len(msg.content) - 1])
      await mem.add_roles(role)
@bot.event
async def on_raw_reaction_remove(reaction):
  serv = discord.utils.get(bot.guilds, id=servId)
  mem = discord.utils.get(serv.members, id=reaction.user_id)
  chan = discord.utils.get(serv.channels, name="roles")
  msg = await chan.fetch_message(reaction.message_id)
  if mem == bot.user:
    return
  if msg:
    if msg.content[len(msg.content)-1] == "*":
      role = discord.utils.get(serv.roles, name=msg.content[:len(msg.content) - 1])
      await mem.remove_roles(role)

@bot.command(name="emergency_shutdown")
@commands.has_any_role("Staff", "Owner")
async def emergency_shutdown(ctx):
  sys.exit()

@bot.command(name="role_setup")
@commands.guild_only()
@commands.has_any_role("Roler")
async def role_react(ctx):
  #role = discord.utils.get(ctx.guild.roles, name=role)
  chan = discord.utils.get(ctx.guild.text_channels, name="roles")
  allMsgs = await chan.history(limit=50).flatten()
  for lMsg in allMsgs:
    if lMsg.content[len(lMsg.content) - 1] == "*":
      await lMsg.add_reaction("🦝")
    
@bot.command(name="help")
async def help(ctx):
  if ctx.channel.name == "moderator-only":
    #Moderators Help commands
    embed=discord.Embed(title="WMAA Bot Help", color=0xcc0000)
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/760194690967535636/805934654045552650/Wmaa_logo.png")
    embed.add_field(name="w!set_nick", value="Set the nickname of yourself or (admin only) others", inline=True)
    embed.add_field(name="w!apply_roles", value="Apply roles on-demand", inline=True)
    embed.add_field(name="w!all_members", value="Print each member in a separate message", inline=True)
    embed.add_field(name="w!role_setup", value="The bot will add a reaction to each message with an * at the end.", inline=True)
    embed.add_field(name="w!emergency_shutdown", value="Kill all bot processes", inline=True)
    embed.set_footer(text="Moderator Help command - version 1.1")
    await ctx.send(embed=embed)
  else:
    embed=discord.Embed(title="WMAA Bot Help", color=0xcc0000)
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/760194690967535636/805934654045552650/Wmaa_logo.png")
    embed.add_field(name="w!set_nick", value="Set your nickname. ", inline=True)
    embed.add_field(name="w!help", value="This help command", inline=True)
    embed.set_footer(text="Basic everybody help command - Version 1.1")
    await ctx.send(embed=embed)

@bot.command(name="apply_roles")
@commands.has_any_role("Roler", "Staff", "Owners", "Fish")
@commands.guild_only()
async def apply_roles(ctx):
  chan = discord.utils.get(ctx.guild.text_channels, name="roles")
  allMsgs = await chan.history(limit=50).flatten()
  for lMsg in allMsgs:
    if lMsg.content[len(lMsg.content)-1] == "*":
      try:
        role = discord.utils.get(ctx.message.guild.roles,name=lMsg.content[:len(lMsg.content) - 1])
      except Exception as e:
        await ctx.send("Error: that role is incorrect. Please make sure you have the role typed in exactly the way it is in Server Settings!")
        print(e)
      reactions = lMsg.reactions
      for lReaction in reactions:
        users = await lReaction.users().flatten()
        for lUser in users:
          print(lUser.display_name)
          print(type(lUser))
          try:
            if not lUser.bot:
              if role not in lUser.roles:
                print("role")
                await lUser.add_roles(role)
          except Exception as e:
            await ctx.send("Error:")
            await ctx.send(e)

#Nickname command (to add to DM strand when user joins)
@bot.command(name="set_nick")
@commands.guild_only()
async def nickname(ctx, name):
  person = ctx.author
  await person.edit(nick=name)

@bot.command(name="dm")
async def dm(ctx):
  await ctx.message.author.send("hello")

#All Members in seperate message command
@bot.command(name="all_members")
@commands.guild_only()
@commands.has_any_role('student')
async def all_members(ctx, exclude:bool=False):
  x = ctx.guild.members
  await ctx.send("Starting... please wait until you see the 'Done' message!")
  for mem in x:
    if mem.bot and exclude == False:
      await ctx.send("*" + mem.display_name + "* BOT")
    elif not mem.bot:
      await ctx.send(mem.display_name)
  await ctx.send("**Done.**")

#On demand testing of the initual DM strand
#WORKING
@bot.command(name="test_join")
async def on_member_jointest(ctx):
  member = ctx.message.author
  server = discord.utils.get(bot.guilds, id=servId)
  modChan = discord.utils.get(server.text_channels, name="moderator-only")
  memobj = discord.utils.get(server.members, id=member.id)
  restrictedAcc = discord.utils.get(server.roles, name="Outside-Aviation")
  await member.send("Hello, and welcome to the Official West Michigan Aviation Academy Discord Server! I'm the main bot in the WMAA server. I manage all roles and many systems within the server. I need a little bit of information from you to get started. Are you a WMAA student, WMAA staff, or neither [Respond with 'student', 'staff', or 'neither']")
  def checkMsg(m):
    return m.author == member and isinstance(m.channel, discord.channel.DMChannel)
  
  try:
    msg = await bot.wait_for('message', check=checkMsg, timeout=300)
  except Exception:
    await member.send("Due to bot limitations, I can only handle DM requests for a max of 5 minutes, and you timed it out. I've given you restricted access and DMed the moderators to handle your case.")
    await modChan.send(member.display_name + " timed out a DM strand. I've given them restricted access in the meantime.")
    await memobj.add_roles(restrictedAcc)
  
  if msg.content == "student" or msg.content == "Student":
    await member.send("Ok cool!")
    await member.send("What is a good nickname that the members in the server can use to talk to you?")
    nickname = await bot.wait_for("message", check=checkMsg)
    await memobj.edit(nick=nickname.content)
    await memobj.add_roles(discord.utils.get(server.roles, name="student"))
    await member.send("Your nickname has been set. Go to the #roles(https://discord.com/channels/695039585180319845/708150431729189005/746498758627295323) channel in the server to set up your roles!")

  elif msg.content == "staff" or msg.content == "Staff":
    await member.send("Hello staff member! I've set up your roles for you. Welcome to the WMAA discord server!")
    await memobj.add_roles(restrictedAcc)
    await modChan.send(member.display_name + " is a staff member. They have the restricted access role given to them currently.")
  elif msg.content == "neither" or msg.content == "Neither":
    await ctx.send("Ok, currently this server is restricted to WMAA students and staff, but I've sent a message to the Admins. If they allow you, they'll give you roles and access to the main channels in the server. ")
    await memobj.add_roles(restrictedAcc)
    await modChan.send(member.display_name + " is trying to join the server. They are not a WMAA student or staff. They have restricted access currently.")
@bot.event
async def on_message(message):
  await bot.process_commands(message)
@bot.event
async def on_command_error(ctx, error):
  if isinstance(error, commands.MissingAnyRole):
    await ctx.send("You are missing roles!")
  elif isinstance(error, commands.NoPrivateMessage):
    await ctx.send("This is a server-only command!")
  else:
    print(error)
#Load token from .env
load_dotenv()
Token = os.getenv("TOKEN")
#Connection
bot.run(Token)
client.run(Token)