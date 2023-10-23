import os, json, discord, time
from discord.ext import commands
from discord.ext.commands import Bot, when_mentioned_or
from datetime import date, datetime
from utils import setup_file

with open('../setup.json') as file:
    setup_file = json.load(file)
    ownerID = setup_file['discord']['owner_id']
    bot_default_prefix = setup_file['discord']['command_prefix']
	
bot_default_game = "{}help to begin.".format(bot_default_prefix)

plugins = []
for file in os.listdir("./plugins"):
    if file.endswith(".py") and not "__init__" in file:
        plugins.append("plugins." + os.path.splitext(file)[0])

odin = True

class ThoughtsEmpty(Bot):

    _myPrefix = bot_default_prefix

    def __init__(self, *args, **kwargs):
    
        intents = discord.Intents.default()
        intents.members = True
        super().__init__(command_prefix=when_mentioned_or(setup_file["discord"]["command_prefix"]),intents=intents,
                         description="distribution disco")
        self.http.user_agent = "ThoughtsEmpty_clone"

    async def on_ready(self):
        print("\nLogged in as:\n\nBot Name: {0.user.name}\nBot ID: {0.user.id}\n\n".format(self))
        print("HOW_DO_I_MAKE_LEMONADE/.\n------------------------------------------------------------".format(self.user.name.upper()))
        global_bot_name = self.user.name
        global_bot_url = self.user.avatar_url
        await self.change_presence(activity=discord.Game(name=bot_default_game))

    async def on_command_error(self, ctx, exception):
        dirPath = "crash/{}/".format(time.strftime("%Y-%m-%d"))
        filePath = dirPath + "errors.log"
        if not os.path.exists(filePath):
            os.mkdir(dirPath)
            open(filePath, 'a').close()
        logf = open(filePath, "a")
        logf.write("{}{}".format(str(exception), "\n[^Invoke performed by user: " + str(ctx.message.author.id) + "]\n\n"))
        if isinstance(exception, commands.errors.CommandNotFound):
            return
        # if isinstance(exception, commands.errors.CheckFailure):
            # await ctx.message.channel.send(embed=discord.Embed(description="This command is restricted.\n{}".format(exception)))
            # return
        if isinstance(exception, commands.errors.CommandOnCooldown):
            await ctx.message.channel.send("{}\nThis command is still on cooldown, wait a bit please.".format(ctx.message.author.mention))
            return

    async def on_member_join(self, member):
        await self.write_tracklog_to_file("JOINS.TXT", message, "JOIN", "-", "/joinmethod()", member.id)
			
    async def on_member_remove(self, member):
        await self.write_tracklog_to_file("JOINS.TXT", message, "QUIT", "-", "/quitmethod()", member.id)

    def run(self):
        print("\n<<<<LOADING PLUGINS>>>>\n")
        for plugin in plugins:
            try:
                self.load_extension(plugin)
                print("{0} is loading...Success".format(plugin))
            except discord.ClientException:
                print("{0} does not have a setup function!".format(plugin))
            except ImportError as IE:
                print(IE)
        print("\n<<<<PLUGINS LOADED>>>>\n\nNow loading login token and connecting to Discord...")
        super().run(setup_file["discord"]["token"])

    async def on_message(self, message):
        await self.write_tracklog_to_file("LOGS.TXT", message, "POST", message.channel, message.content, message.author.id)
        await bot.process_commands(message)

    async def on_error(event, *args, **kwargs):
        pass
		
    async def on_message_delete(self, message):
        if not isinstance(message.channel, discord.abc.PrivateChannel):
            await self.write_tracklog_to_file("LOGS.TXT", message, "DELETE", message.channel, message.content, message.author.id)

    async def on_message_edit(self, message, newMessage):
        if not isinstance(message.channel, discord.abc.PrivateChannel):
            outputString = "{}{}EDITED: {}".format(message.content, "\n", newMessage.content)
            await self.write_tracklog_to_file("LOGS.TXT", message, "EDIT", message.channel, outputString, message.author.id)
                
    #odinseye
    async def write_tracklog_to_file(self, fn, message, type, channel, content, id):
        if not odin: return
            try:
                self.write_tracklog_to_logfile(fn, type, channel.name, content, message.author)
            except Exception as e:
                print(e)
            
    def write_tracklog_to_logfile(self, fileName, type, channel, content, user):
        dirPath = "ODINSEYE/"
        filePath = dirPath + fileName
        newLineChar = u"\r\n"
        if not os.path.exists(filePath):
            open(filePath, 'a').close()
        logf = open(filePath, "ab")
        logf.write("DATE: {0}{5}USERID: {6}{5}USER: {1}{5}ACTION: {2}{5}CHANNEL: {3}{5}CONTENT: {4}{5}{5}".format(str(datetime.now())[:str(datetime.now()).index(".")], user.name, type, channel, content, newLineChar, user.id).encode('utf-8'))
        logf.close()
		
if __name__ == "__main__":
    bot = ThoughtsEmpty()
    bot.run()