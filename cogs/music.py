import discord
from discord.ext import commands

from youtube_dl import YoutubeDL

class music_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.is_playing = False
        self.is_paused = False

        self.music_queue = []
        self.YDL_OPTIONS = {'format' : 'bestaudio', 'noplaylist' : 'True'}
        self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnected_streamed ` -reconnect_delay_max 5', 'options': '-vn'}

        self.vc = None

    def search_yt(self,item):
        with YoutubeDL(self.YDL_OPTIONS) as ydl:
            try:
                info = ydl.extract_info("ytsearch:%s" % item, download=False)['entries'][0]
            except Exception:
                return False
        return {'source': info['formats'][0]['url'], 'title': info['title']}

    
    def play_next(self):
        if len(self.music_queue) > 0:
            self.is_playing = True

            m_url = self.music_queue[0][0]['source']

            self.music_queue.pop(0)

            self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next())
        else:
            self.is_playing = False

    async def play_music(self,ctx):
        if len(self.music_queue > 0):
            self.is_playing = True
            m_url = self.music_queue[0][0]['source']

            if self.vc == None or not self.vc.is_connected():
                self.vc = await self.music_queue[0][1].connect()

                if self.vc == None:
                    await ctx.send("could not connect to the voice channel.")
            else:
                await self.vc.move_to(self.music_queue[0][1])

            self.music_queue.pop(0)

            self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next())
        else:
            self.is_playing = False

    @commands.command(name="play", alises=["p", "playing"], help="play the selected song from youtube")
    async def play(self, ctx, *args):
        query = " ".join(args)

        voice_channel = ctx.author.voice.channel
        if voice_channel is None:
            await ctx.send("connect to a voice channel!")
        elif self.is_paused:
            self.vc.resume()
        else:
            song = self.search_yt(query)
            if type(song) == type(True):
                await ctx.send("couldn't download the song. incorrect format, try a different keyword.")
            else:
                await ctx. send("song has been added to the queue.")
                self.music_queue.apped([song, voice_channel])
                
                if self.is_playing == False:
                    await self.play_music(ctx)

    @commands.command(name="pause", help="pauses the current song being played")
    async def pause(self, ctx, *args):
        if self.is_playing:
            self.is_playing = False
            self.is_paused = True
            self.vc.pause()
        elif self.is_paused:
            self.is_playing = True
            self.is_paused = False
            self.vc.resume()
        
    @commands.command(name="resume", help="resumes playing the current song being played")
    async def resume(self, ctx, *args):
        if self.is_paused:
            self.is_playing = True
            self.is_paused = False
            self.vc.resume()
    
    @commands.command(name="skip", help="skips the song that is currently being played")
    async def skip(self, ctx, *args):
        if self.vc != None and self.vc:
            self.vc.stop()
            await self.play_music(ctx)

    @commands.command(name="queue", help="displays all songs currecntly in the queue")
    async def queue(self, ctx):
        retval = ""

        for i in range(0, len(self.music_queue)):
            if i > 4: break
            retval += self.music_queue[i][0]['title'] + '\n'

        if retval != "":
            await ctx.senf(retval)
        else:
            await ctx.send("no music in the queue.")

    @commands.command(name="clear", aliases=["c", "bin"], help="stops the current song and clears the queue")
    async def clear(self, ctx, *args):
        if self.vc != None and self.is_playing:
            self.vc.stop()
        self.music_queue = []
        await ctx.send('music queue cleared.')

    @commands.command(name="leave", aliases=["d", "disconnect"], help="kicks the bot from the voice channel")
    async def leave(self, ctx):
        self.is_playing = False
        self.is_paused = True
        await self.vc.disconnect()
        

# 0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000

# import discord
# from discord.ext import commands
# import youtube_dl
# import nacl

# bot = commands.Bot(command_prefix = '!', intents=discord.Intents.all()) 

# intents = discord.Intents.default()
# intents.members = True
# intents.message_content = True

# class music(commands.Cog):
#     def __init__(self, bot):
#         self.client = bot

# def setup(client):
#     client.add_cog(music(bot))

# @commands.command()
# async def join(self,ctx):
#     if ctx.author.voice is None:
#         await ctx.send("you're not in a voice channel!")
#         voice_channel = ctx.author.voice.channel
#     if ctx.voice_client is None:
#         await voice_channel.connect()
#     else:
#         await ctx.voice_client.move_to(voice_channel)

# @commands.command()
# async def disconnect(self,ctx):
#     await ctx.voice_client.disconnect()  

# @commands.command()
# async def play (self, ctx, url):
#     ctx.voice_client.stop()
#     FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
#     YDL_OPTIONS = {'format':"bestaudio"}
#     vc = ctx.voice_bot

#     with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
#         info = ydl.extract_info(url, download=False)
#         url2 = info['formats'][0]['url']
#         source = await discord.FFmpegOpusAudio.from_probe(url2, **FFMPEG_OPTIONS)
#         vc.play(source)

# @commands.command()
# async def pause(self,ctx):
#     await ctx.voice_client.pause()
#     await ctx.send('paused.')

# @commands.command()
# async def resume(self,ctx):
#     await ctx.voice_client.resume()
#     await ctx.send('resumed.')


# def setup(bot):
#     bot.add_cog(music(bot))

            