import io
import inspect
import shutil
import traceback
from contextlib import redirect_stdout

import discord
from discord.ext import commands
from utils.checks import is_owner


class Owner(commands.Cog):
    """A set of commands only for the owner of the bot"""

    def __init__(self, bot):
        self.bot = bot
        self.sessions = set()

    @commands.check(is_owner)
    @commands.command(name="setgame")
    async def game_change(self, ctx, *, ngame: str):
        """Lets the bot owner change the game of the bot"""
        await self.bot.change_presence(activity=discord.Game(name=ngame))
        print('Game has now been changed to: {}'.format(ngame))

    @commands.check(is_owner)
    @commands.command(name="setavatar")
    async def owner_set_avatar(self, ctx, fileName: str):
        """Lets the bot owner change the avatar of the bot"""
        with open(fileName, 'rb') as image:
            image = image.read()
            await self.bot.user.edit(avatar=image)
            print("My avatar has been changed!")
			
    @commands.check(is_owner)
    @commands.command(name="ping")
    async def owner_gets_pinged(self, ctx):
        await ctx.send('pong')
		
    @commands.check(is_owner)
    @commands.command(name='reload', hidden=True)
    async def owner_reload(self, ctx, *, cog: str):
        cogsRoot = "plugins." + cog
        try:
            self.bot.unload_extension(cogsRoot)
            self.bot.load_extension(cogsRoot)
        except Exception as e:
            await ctx.send('Error reloading cog {}: {type(e).__name__} - {}'.format(cog,e))
        else:
            await ctx.send('Cog {} reloaded.'.format(cog))
		
    @commands.check(is_owner)
    @commands.command(name="respond", pass_context=True)
    async def owner_bot_responds(self, ctx, channelString, *, message:str=""):
        targetChannel = ctx.message.channel_mentions[0]
        targetMessage = message
        if not targetChannel: return
        await ctx.message.delete()
        await targetChannel.send(targetMessage)
			
    @commands.check(is_owner)
    @commands.command(name="reboot")
    async def owner_shutdown(self, ctx):
        #await self.bot.say('Yessir.')
        #await self.bot.say(':gun: - Bang')
        em = discord.Embed(title="Rebooting", description="", colour=0x00AE86)
        await ctx.send(embed=em)
        await self.bot.close()
		
    @commands.check(is_owner)
    @commands.command(name="ping")
    async def owner_gets_pinged(self, ctx):
        await ctx.send('pong')
		
    @commands.check(is_owner)
    @commands.command(name="servlink")
    async def owner_server_link(self, ctx):
        linkURL = "https://discordapp.com/oauth2/authorize?client_id={}&scope=bot&permissions=0".format(self.bot.user.id)
        em = discord.Embed(title="Click here to invite me elsewhere!", description="Discord will tell you links are spoopy. This one isn't.", colour=0x00AE86)
        em.url = linkURL
        await ctx.send(embed=em)

    @commands.check(is_owner)	
    @commands.command(name="sinfo")
    async def guild_info(self, ctx):
        """Gets information about the current server"""
        await ctx.send("```http\n"
                           "Server: {0}\n"
                           "ID: {0.id}\n"
                           "Region: {0.region}\n"
                           "Created: {0.created_at}\n"
                           "Member Count: {1}\n"
                           "Owner: {0.owner}\n"
                           "Icon: {0.icon_url}\n"
                           "Roles: {2}"
                           "```".format(ctx.message.guild, sum(1 for x in ctx.message.guild.members),
                                        ", ".join([x.name for x in ctx.message.guild.roles])))
                                        
    @commands.check(is_owner)
    @commands.command(name="uinfo")
    async def user_info(self, ctx, user: discord.Member = None):
        """Gets information about the desired user (defaults to the message sender)"""
        #print("do")
        try:
            if not user:
                user = ctx.message.author
            msg = "```\n"
            msg += "User: %s\n" % user.name
            msg += "Nickname %s\n" % user.nick
            msg += "ID: %s\n" % user.id
            msg += "Created at: %s\n" % user.created_at
            msg += "Joined on: %s\n" % user.joined_at
            msg += "Roles: %s\n" % ", ".join([role.name for role in user.roles if role.name != "@everyone"])
            msg += "```\n"
            msg += "Avatar: %s" % user.avatar_url
            await ctx.send(msg)
        except Exception as e:
            print(e)
			
def setup(bot):
    bot.add_cog(Owner(bot))
