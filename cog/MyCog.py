import os
import math

import discord
from discord.ext import tasks, commands
from datetime import datetime

from src.MyModules import MyModules as myMod


class MyCog(commands.Cog):

    def __init__(self, bot):
        self.general_text_channel_id = int(os.getenv('GENERAL_TEXT_CHANNEL_ID'))
        self.bot = bot
        self.bot_id = int(os.getenv('BOT_ID'))
        self.emperor_id = int(os.getenv('EMPEROR_ID'))
        self.icon_url = 'https://cdn.discordapp.com/avatars/{id}/{avatar}.png'
        # self.sleep_alert.start()

    @commands.command(name='のんだ')
    async def drug(self, ctx, drug_name: str, amount: float):

        mod = myMod()
        user = ctx.author
        bot = self.bot.get_user(self.bot_id)
        embed_description = f"{user} took '{drug_name} {amount}mg' at {datetime.now().strftime('%H:%M')}"

        bot_icon = self.icon_url.format(
            id=str(self.bot_id),
            avatar=bot.avatar,
        )

        icon = self.icon_url.format(
            id=str(ctx.author.id),
            avatar=ctx.author.avatar,
        )

        amount = math.floor(amount * 10 ** 2) / (10 ** 2)

        if amount <= 0:
            emperor = self.bot.get_user(self.emperor_id)
            embed = discord.Embed(title='のんだ', description='飲んでねぇだろ', color=0xff4dd8)
            embed.set_author(name=bot, icon_url=bot_icon)
            reportToTheThrone = (
                "今日かくの如き自体を招き、\n"
                "陛下の御心を騒がせ奉りました事は"
                "臣の不明の致しますところ、\n"
                "誠に慚愧に耐えません。\n"
            )
            embed.add_field(name="失敗", value=f"{reportToTheThrone}{emperor.mention}", inline=True)
            await ctx.send(embed=embed)
            return False

        amount = math.floor(amount * 10 ** 2) / (10 ** 2)

        if not mod.save_use_drug_history(user.id, drug_name, amount):
            embed = discord.Embed(title='のんだ', description='飲むな', color=0xff4dd8)
            embed.set_author(name=bot, icon_url=bot_icon)
            embed.add_field(name="失敗", value="登録されていない薬物です", inline=True)
            await ctx.send(embed=embed)
            return False

        embed = discord.Embed(title='のんだ', description=embed_description, color=0xff4dd8)
        embed.set_author(name=user, icon_url=icon)
        embed.set_thumbnail(url=bot_icon)
        embed.set_footer(text='NewWorldHandyman')
        await ctx.send(embed=embed)

    @commands.command(name='薬物登録')
    async def save_drug_data(self, ctx, drug_name: str):

        mod = myMod()
        user = ctx.author.name
        bot = self.bot.get_user(self.bot_id)
        embed_description = f"{drug_name}を登録しました"

        bot_icon = self.icon_url.format(
            id=str(self.bot_id),
            avatar=bot.avatar,
        )

        icon = self.icon_url.format(
            id=str(ctx.author.id),
            avatar=ctx.author.avatar,
        )

        if not mod.save_drug_mapping_data(drug_name):
            embed = discord.Embed(title='薬物登録', description='見てるんだぞ', color=0xff4dd8)
            embed.set_author(name=bot, icon_url=bot_icon)
            embed.add_field(name="失敗", value="登録できない薬物です", inline=True)
            await ctx.send(embed=embed)
            return False

        embed = discord.Embed(title='薬物登録', description=embed_description, color=0xff4dd8)
        embed.set_author(name=user, icon_url=icon)
        embed.set_thumbnail(url=bot_icon)
        embed.set_footer(text='NewWorldHandyman')

        await ctx.send(embed=embed)

    @commands.command()
    async def hello(self, ctx):
        await ctx.send('Handyman is watching you')

    @commands.command(name='薬物使用履歴')
    async def drug_use_history_list_by_user(self, ctx, arg):
        mod = myMod()
        bot = self.bot.get_user(self.bot_id)

        icon = self.icon_url.format(
            id=str(self.bot_id),
            avatar=bot.avatar,
        )

        embed_description = '>>> '
        list_by_user = mod.get_drug_use_history(arg)

        if not list_by_user:
            await ctx.send(f'<@{str(ctx.author.id)}> Who that it?')
            return False

        for row in list_by_user:
            embed_description += f"{row['user']}: {row['drug_name']} {row['amount']}mg at {row['created_at']}\n"

        embed = discord.Embed(title=f'drug use history by {arg}', description=embed_description, color=0xff4dd8)
        embed.set_author(name='NewWorldHandyman', icon_url=icon)
        await ctx.send(embed=embed)

    @commands.command(name='使用薬物リスト')
    async def drug_use_count_list_by_user(self, ctx, arg):
        mod = myMod()
        bot = self.bot.get_user(self.bot_id)

        icon = self.icon_url.format(
            id=str(self.bot_id),
            avatar=bot.avatar,
        )

        embed_description = '>>> '
        list_by_user = mod.get_drug_use_count(arg)

        if not list_by_user:
            await ctx.send(f'<@{str(ctx.author.id)}> Who that it?')
            return False

        for row in list_by_user:
            embed_description += f"{row['user']}: {row['drug_name']} {row['count']}回 総量-{row['amount']}mg\n"

        embed = discord.Embed(title=f'drug use count list by {arg}', description=embed_description, color=0xff4dd8)
        embed.set_author(name='NewWorldHandyman', icon_url=icon)
        await ctx.send(embed=embed)

    @commands.command(name='薬物一覧')
    async def get_registerd_drug_list(self, ctx):
        mod = myMod()
        bot = self.bot.get_user(self.bot_id)
        icon = self.icon_url.format(
            id=str(self.bot_id),
            avatar=bot.avatar,
        )

        embed_description = '>>> '
        list_by_user = mod.get_registered_drug_list()

        for row in list_by_user:
            embed_description += f"{row['drug']}\n"

        embed = discord.Embed(title=f'registerd drug list', description=embed_description, color=0xff4dd8)
        embed.set_author(name='NewWorldHandyman', icon_url=icon)
        await ctx.send(embed=embed)

    @commands.command(name='キマってきた')
    async def effect_manifestation(self, ctx):
        mod = myMod()
        bot = self.bot.get_user(self.bot_id)
        user = ctx.author.name

        the_last_time_of_medication = mod.get_the_last_time_of_medication(user)

        bot_icon = self.icon_url.format(
            id=str(self.bot_id),
            avatar=bot.avatar,
        )

        icon = self.icon_url.format(
            id=str(ctx.author.id),
            avatar=ctx.author.avatar,
        )
        time = datetime.now() - the_last_time_of_medication[0]['created_at']
        minutes = (time.seconds % 3600) // 60
        embed_description = 'It took {} minutes to get trip'.format(minutes)
        embed = discord.Embed(title='キマるな', description=embed_description, color=0xff4dd8)
        embed.set_author(name=user, icon_url=icon)
        embed.set_thumbnail(url=bot_icon)
        embed.set_footer(text='NewWorldHandyman')
        await ctx.send(embed=embed)

    # 毎晩2時に睡眠アラートを流す -> 形骸化の為廃止(2020/09/18)
    '''@tasks.loop(minutes=1)
    async def sleep_alert(self):
        now = datetime.now().strftime('%H:%M')
        if now == '02:00':
            channel = self.bot.get_channel(self.general_text_channel_id)
            await channel.send('寝ろ')

    @sleep_alert.before_loop
    async def before_sleep_alert(self):
        print('waiting...')
        await self.bot.wait_until_ready()
    '''

    @commands.command()
    async def member(self, ctx):
        for member in ctx.guild.members:
            await ctx.send(member.name)

    @commands.command()
    async def member_register(self, ctx):
        mod = myMod()

        member = {
            'user_id': str(ctx.author.id),
            'name': ctx.author.display_name,
            'icon_url': self.icon_url.format(id=ctx.author.id, avatar=ctx.author.avatar),
            'password': '',
        }

        mod.member_register(member)

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        print('test')


def setup(bot):
    bot.add_cog(MyCog(bot))
