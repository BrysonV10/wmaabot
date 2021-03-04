import discord
from discord.ext import commands
intents = discord.Intents.default()
intents.members = True
intents.reactions = True
bot = commands.Bot(command_prefix="w!", intents=intents)
client = discord.Client()
bot.remove_command("help")
class List_Members(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
  @bot.group()
  @commands.guild_only()
  @commands.has_any_role('student')
  async def list_members(self, ctx):
    if ctx.invoked_subcommand is None:
      x = ctx.guild.members
      await ctx.send("Starting... please wait until you see the 'Done' message! (Bots and outside-aviation are included)")
      for mem in x:
        if mem.bot:
          await ctx.send("*" + mem.display_name + "* BOT")
        elif not mem.bot:
          await ctx.send(mem.display_name)
      await ctx.send("**Done.**")
  @list_members.command()
  @commands.guild_only()
  @commands.has_any_role('student')
  async def no_bots(self, ctx):
    x = ctx.guild.members
    await ctx.send("Starting... please wait until you see the 'Done' message! (outside-aviation is included)")
    for mem in x:
      if not mem.bot:
        await ctx.send(mem.display_name)
    await ctx.send("**Done.**")
  @list_members.command()
  @commands.guild_only()
  @commands.has_any_role("student")
  async def no_outside(self, ctx):
    x = ctx.guild.members
    restRole = discord.utils.get(ctx.guild.roles, name="Outside-Aviation")
    await ctx.send("Starting... please wait until you see the 'Done' message! (outside-aviation is not included)")
    for mem in x:
      if not mem.bot:
        if restRole not in mem.roles:
          await ctx.send(mem.display_name)
    await ctx.send("**Done.**")
def setup(bot):
  bot.add_cog(List_Members(bot))