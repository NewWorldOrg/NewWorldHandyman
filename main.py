from discord.ext import commands
import configparser
import os
import src.py_modules.MyCog as myCog

class DiscordClient(commands.Bot):

    def __init__(self, command_prefix):
        super().__init__(command_prefix)
        cog_list = [
            'src.py_modules.MyCog'
        ]
        for cog in cog_list:
            try:
                self.load_extension(cog)
            except Exception as e:
                print(e)

    async def drug_use_history_logger(self, drug_name, channel):
        await channel.send(drug_name)

    async def on_ready(self):
        print("I'm ready !")

    async def on_message(self, message):

        await self.process_commands(message)
        # ヤクブーツ使用記録用コマンド
        '''if '!のんだ ' in message.content:
           #message.channel.send(send'ok')
           msg = message.content
           await self.drug_use_history_logger(msg.replace('!のんだ ', ''), message.channel)
        '''
def main():

    base = os.path.dirname(os.path.abspath(__file__))
    conf_path = os.path.normpath(os.path.join(base))
    conf = configparser.ConfigParser()
    conf.read(conf_path+'/config.ini', encoding='utf-8')
    client = DiscordClient(command_prefix='$')
    client.run(conf['DEFAULT']['BOT_TOKEN'])

if __name__ == '__main__':
    main()
