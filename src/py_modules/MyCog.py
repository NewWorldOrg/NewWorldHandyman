from discord.ext import tasks, commands
import discord
import configparser
import os
from datetime import datetime

class MyCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        base = os.path.dirname(os.path.abspath(__file__))
        conf_path = os.path.normpath(os.path.join(base, '../../'))
        conf = configparser.ConfigParser()
        conf.read(conf_path+'/config.ini', encoding='utf-8')
        self.general_text_channel_id = int(conf['NEW_WORLD']['GENERAL_TEXT_CHANNEL_ID'])
        self.sleep_alert.start()

    @commands.command(name='のんだ')
    async def drug(self, ctx, arg):
        await ctx.send(f'{arg}, {ctx.author.name}')

    @commands.command()
    async def hello(self, ctx):
        await ctx.send('Handyman is watching you')

    @tasks.loop(seconds=1)
    async def sleep_alert(self):
        now = datetime.now().strftime('%H:%M')
        if now == '02:00':
            channel = self.bot.get_channel(self.general_text_channel_id)
            await channel.send('寝ろ')

    @sleep_alert.before_loop
    async def before_sleep_alert(self):
        print('waiting...')
        await self.bot.wait_until_ready()


def setup(bot):
    bot.add_cog(MyCog(bot))
