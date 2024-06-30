import discord
from discord.ext import commands

class help_cog(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        self.help_message = """
```
General commands:
!help - displays all available commands
!hello - well wishes for the day
!goodbye - temporary farewell for the next
!join - bot joins voice channel
!leave - bot leaves voice channel

Admin commands:
!kick - kicks member from server
!ban - bans member from server
!unban - unbans member from server
!addRole - adds member to a role (@user + role)
!removeRole - removes member to a role (@user + role)

Options commands (nfa):
!open - notifies members of newly opened options contracts
!scale - notifies members of trimmed contracts
!close - notifies members of closed options contracts 
```
"""

# !p - finds the song on youtube and plays it in the current channel
# !q - displays the current music queue
# !skip - skips the current song being played
# !clear - stops the music and clears the queue
# !leave - disconnects the bot from the voice channel
# !pause - pauses the current song being played od results if already paused
# !resume - resumes playing the current song

        self.text_channel_text = []
    
    @commands.Cog.listener()
    async def on_read(self):
        for guild in self.bot.guilds:
            for channel in guild.text_channels:
                self.text_channel_text.append(channel)

            await self.send_to_all(self.help_message)
    
    async def send_to_all(self, msg):
        for text_channel in self.text_channel_text:
            await text_channel.send(msg)

    @commands.command(name="help", help="displays all the available commands")
    async def help(self, ctx):
        await ctx.send(self.help_message)