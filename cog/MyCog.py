import configparser
import os

import discord
from discord.ext import tasks, commands
from datetime import datetime

from src.MyModules import MyModules as myMod

class MyCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        base = os.path.dirname(os.path.abspath(__file__))
        conf_path = os.path.normpath(os.path.join(base, '../'))
        conf = configparser.ConfigParser()
        conf.read(conf_path+'/config.ini', encoding='utf-8')
        self.general_text_channel_id = int(conf['NEW_WORLD']['GENERAL_TEXT_CHANNEL_ID'])
        self.sleep_alert.start()

    @commands.command(name='のんだ')
    async def drug(self, ctx, arg):
        mod = myMod()
        user = ctx.author.name

        if not mod.save_use_drug_history(user, arg):
            await ctx.send('薬物の検出ができません')

        await ctx.send(f'{arg}, {user}')

    @commands.command()
    async def hello(self, ctx):
        await ctx.send('Handyman is watching you')

    # 毎晩2時に睡眠アラートを流す
    @tasks.loop(minutes=1)
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