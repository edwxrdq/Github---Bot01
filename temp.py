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
import requests
import json
# import os


intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix = '!', intents=discord.Intents.all()) 



@bot.event 
async def on_ready(): 
    await bot.change_presence(status=discord.Status.idle, activity=discord.Streaming(name='NewJeans', url='https://www.youtube.com/watch?v=ft70sAYrFyY&ab_channel=HYBELABELS'))
    print("The bot is now ready for use!")
    print("-----------------------------")  

@bot.command()
async def hello(ctx):
    await ctx.send("hello, i am the first bot.")

@bot.command()
async def goodbye(ctx):
    await ctx.send("goodbye, have a great rest of the day!")

#detects when user joins server, then runs the following
@bot.event
async def on_member_join(member):
    await channel.send("someone has joined the server!")
    # await channel.send(f"welcome to the server {member.mention}")
    channel = bot.get_channel(1218445506049478659)


#detects when user leaves server, then runs the following
@bot.event
async def on_member_remove(member):
    channel = bot.get_channel(1218445506049478659)
    await channel.send("someone has left the server!")
    # await channel.send(f'{member.mention} has left the server!')

@bot.command(pass_context = True)
async def join(ctx):
    #relies on user input
    if (ctx.author.voice):
        channel = ctx.message.author.voice.channel
        await channel.connect()
    else:
        await ctx.send("you must be in a voice channel to run this command.")


@bot.command(pass_context = True)
async def leave(ctx):
    #if the bot is in a voice channel, it'll run the following command; disconnects then sends message in chat
    if (ctx.voice_client):
        #guild = server, voice client = removes from the channel the bot's in
        await ctx.guild.voice_client.disconnect()
        await ctx.send("i've left the voice channel.")
    else:
        #if bot isn't in a voice channel then it'll run this
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
async def embed(ctx):
    embed = discord.Embed(title="dog", url="http://google.com", description="we love dogs", color=0x967bb6)
    embed.set_author(name=ctx.author.display_name, url="http://google.com")
    embed.add_field(name="shorkie", value="nico", inline=False)
    embed.add_field(name="shorkie", value="chewy", inline=False)
    embed.set_footer(text="thank you for reading")
    await ctx.send(embed=embed)

bot.run(DISCORD_TOKEN)