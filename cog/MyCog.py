import configparser
import os

import discord
from discord.ext import tasks, commands
from datetime import datetime

from src.MyModules import MyModules as myMod

class MyCog(commands.Cog):

    def __init__(self, bot):
        base = os.path.dirname(os.path.abspath(__file__))
        conf_path = os.path.normpath(os.path.join(base, '../'))
        conf = configparser.ConfigParser()
        conf.read(conf_path+'/config.ini', encoding='utf-8')
        self.general_text_channel_id = int(conf['NEW_WORLD']['GENERAL_TEXT_CHANNEL_ID'])
        self.bot = bot
        self.bot_id = int(conf['DEFAULT']['BOT_ID'])
        self.icon_url = 'https://cdn.discordapp.com/avatars/{id}/{avatar}.png'
        self.sleep_alert.start()

    @commands.command(name='のんだ')
    async def drug(self, ctx, arg):

        mod = myMod()
        user = ctx.author.name
        bot  = self.bot.get_user(self.bot_id)
        embed_description = f"{user} took '{arg}' at {datetime.now().strftime('%H:%M')}"

        bot_icon = self.icon_url.format(
            id = str(self.bot_id),
            avatar = bot.avatar,
        )

        icon = self.icon_url.format(
            id = str(ctx.author.id),
            avatar = ctx.author.avatar,
        )

        embed=discord.Embed(title='のんだ', description=embed_description, color=0xff4dd8)
        embed.set_author(name=user, icon_url=icon)
        embed.set_thumbnail(url=bot_icon)
        embed.set_footer(text='NewWorldHandyman')
        if not mod.save_use_drug_history(user, arg):
            embed.add_field(name="", value="薬物の検出に失敗しました", inline=True)
            await ctx.send(embed=embed)

        await ctx.send(embed=embed)

    @commands.command()
    async def hello(self, ctx):
        await ctx.send('Handyman is watching you')

    @commands.command(name='薬物使用履歴')
    async def drug_use_history_list_by_user(self, ctx, arg):
        mod = myMod()
        bot = self.bot.get_user(self.bot_id)

        icon = self.icon_url.format(
            id = str(self.bot_id),
            avatar = bot.avatar,
        )

        embed_description = '>>> '
        list_by_user = mod.get_drug_use_history(arg)

        if not list_by_user:
            await ctx.send(f'<@{str(ctx.author.id)}> Who that it?')
            return False

        for row in list_by_user:
            embed_description += f"{row['user']}: {row['drug_name']} at {row['created_at']}\n"

        embed = discord.Embed(title=f'drug use history by {arg}', description=embed_description, color=0xff4dd8)
        embed.set_author(name='NewWorldHandyman', icon_url=icon)
        await ctx.send(embed=embed)

    @commands.command(name='使用薬物リスト')
    async def drug_use_count_list_by_user(self, ctx, arg):
        mod = myMod()
        bot = self.bot.get_user(self.bot_id)

        icon = self.icon_url.format(
            id = str(self.bot_id),
            avatar = bot.avatar,
        )

        embed_description = '>>> '
        list_by_user = mod.get_drug_use_count(arg)

        if not list_by_user:
            await ctx.send(f'<@{str(ctx.author.id)}> Who that it?')
            return False

        for row in list_by_user:
            embed_description += f"{row['user']}: {row['drug_name']} {row['count']}回\n"

        embed = discord.Embed(title=f'drug use count list by {arg}', description=embed_description, color=0xff4dd8)
        embed.set_author(name='NewWorldHandyman', icon_url=icon)
        await ctx.send(embed=embed)


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
