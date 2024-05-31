import discord
from discord.ext import commands 
from discord import FFmpegPCMAudio
from os import getenv
#dotenv = essentially invisible file that stores the info, so it's not committed
from dotenv import load_dotenv
load_dotenv()
DISCORD_TOKEN = getenv('BOTKEY')
from discord import Member
from discord.ext.commands import has_permissions, MissingPermissions
from discord.utils import get
import requests
import json
# import os


intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix = '!', intents=discord.Intents.all()) 



@bot.event 
async def on_ready(): 
    # await bot.change_presence(status=discord.Status.idle, activity=discord.Streaming(name='NewJeans', url='https://www.youtube.com/watch?v=ft70sAYrFyY&ab_channel=HYBELABELS'))
    print("bot has connected to the server!")

@bot.command()
async def hello(ctx):
    await ctx.send("hello, let's make some progress today!")

@bot.command()
async def goodbye(ctx):
    await ctx.send("goodbye, let's work harder next time!")

@bot.event
async def on_member_join(member):
    # await channel.send("someone has joined the server!")
    await channel.send(f"{member.mention} has joined the server!")
    channel = bot.get_channel(1218445506049478659)

@bot.event
async def on_member_remove(member):
    channel = bot.get_channel(1218445506049478659)
    # await channel.send("someone has left the server!")
    await channel.send(f'{member.mention} has left the server!')

@bot.command(pass_context = True)
async def join(ctx):
    if (ctx.author.voice):
        channel = ctx.message.author.voice.channel
        await channel.connect()
    else:
        await ctx.send("you must be in a voice channel to run this command.")

@bot.command(pass_context = True)
async def leave(ctx):
    if (ctx.voice_client):
        await ctx.guild.voice_client.disconnect()
        await ctx.send("i've left the voice channel.")
    else:
        await ctx.send("i'm not in a voice channel.")

@bot.listen('on_message')
async def on_message(message):
    if message.content.casefold() == "nigga":
        await message.delete()
        await message.channel.send("that language is not allowed in this server!")

@bot.command()
@has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f'user {member} has been kicked.')

@kick.error
async def kick_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("you don't have permission to kick people.")

@bot.command()
@has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f'user {member} has been banned.')

@ban.error
async def ban_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("you don't have permission to ban people.")

@bot.command()
@has_permissions(ban_members=True)
async def unban(ctx, member: discord.Member, *, reason=None):
    banned_users = await ctx.guild.bans()
    print(banned_users)
    member_name, member_discriminator = member.split("#")

    for ban_entry in banned_users:
        print(ban_entry)
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'unbanned {user.mention}.')
    await member.ban(reason=reason)
    await ctx.send(f'user {member} has been banned.')

# @bot.event
# async def on_command_error(ctx, error):
#     if isinstance(error, commands.MissingPermissions):
#         await ctx.send("you don't have permissions to run this command.")

@unban.error
async def unban_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("you don't have permission to unban people.")

@bot.command()
async def embed(ctx):
    embed = discord.Embed(title="dog", url="http://google.com", description="we love dogs", color=0x967bb6)
    embed.set_author(name=ctx.author.display_name, url="http://google.com")
    embed.add_field(name="shorkie", value="nico", inline=False)
    embed.add_field(name="shorkie", value="chewy", inline=False)
    embed.set_footer(text="thank you for reading")
    await ctx.send(embed=embed)

@bot.command()
async def message(ctx, user:discord.Member, *, message=None):
    message = "welcome to the server!"
    embed = discord.Embed(title=message)
    await user.send(embed=embed)

# @bot.event
# async def on_member_remove(member):
#     channel = bot.get_channel(1218445506049478659)
#     await channel.send('goodbye' + member + '!')

@bot.event
async def on_reaction_add(reaction, user):
    channel = reaction.message.channel
    await channel.send(user.name + " added: " + reaction.emoji)

@bot.event
async def on_reaction_remove(reaction, user):
    channel = reaction.message.channel
    await channel.send(user.name + " removed: " + reaction.emoji)

@bot.command(pass_context = True)
@has_permissions(manage_roles = True)
async def addRole(ctx, user : discord.Member, *, role : discord.Role):
    if role in user.roles:
        await ctx.send(f"{user.mention} already has this role.")
    else:
        await user.add_roles(role)
        await ctx.send(f"{user.mention} has been added to the {role} role.")

@addRole.error
async def role_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("you don't have permissions to add roles.")

@bot.command(pass_context = True)
@has_permissions(manage_roles = True)
async def removeRole(ctx, user : discord.Member, *, role : discord.Role):
    if role in user.roles:
        await user.remove_roles(role)
        await ctx.send(f"removed {user.mention} from the {role} role.")
    else:
        await ctx.send(f"{user.mention} doesn't have the {role} role.")

@removeRole.error
async def removeRole_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("you don't have permissions to add roles.")

bot.run(DISCORD_TOKEN)