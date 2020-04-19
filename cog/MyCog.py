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
        embed_description = f"{user} took '{arg}' at {datetime.now().strftime('%H:%M')}"
        icon = f'https://cdn.discordapp.com/avatars/{str(ctx.author.id)}/{ctx.author.avatar}.png'
        embed=discord.Embed(title='のんだ', description=embed_description, color=0xff4dd8)
        embed.set_author(name=user, icon_url=icon)
        embed.set_thumbnail(url="https://cloud.mogamin.net/apps/files_sharing/publicpreview/Q56wtgd8x2SEoXk?fileId=299&file=%2FEQ9n5UUUEAAYwTR.jpeg&x=1680&y=1050&a=true")
        embed.set_footer(text='NewWorldHandyman')
        if not mod.save_use_drug_history(user, arg):
            embed.add_field(name="", value="薬物の検出に失敗しました", inline=True)
            await ctx.send(embed=embed)

        await ctx.send(embed=embed)

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
