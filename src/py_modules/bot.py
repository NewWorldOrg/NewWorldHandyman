import discord

class DiscordClient(discord.Client):

    async def drug_use_history_logger(self, drug_name, channel):
        await channel.send(drug_name)

    async def on_ready(self):
        print("I'm ready !")

    async def on_message(self, message):
        if '!のんだ ' in message.content:
           message.channel.send('ok')
           msg = message.content
           await self.drug_use_history_logger(msg.replace('!のんだ ', ''), message.channel)

