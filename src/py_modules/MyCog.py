from discord.ext import commands
import discord

class MyCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        print('MyCog')

    @commands.command(name='のんだ')
    async def drug(self, ctx, *arg):
        await ctx.send(f'drug! {arg} {ctx.author.name}')

    @commands.command()
    async def hello(self, ctx):
        await ctx.send('Handyman is watching you')

def setup(bot):
    bot.add_cog(MyCog(bot))
