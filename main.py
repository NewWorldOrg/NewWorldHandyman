from discord.ext import commands
import configparser
import os

class MyBot(commands.Bot):

    def __init__(self, command_prefix):
        super().__init__(command_prefix)
        cog_list = [
            'cog.MyCog'
        ]
        for cog in cog_list:
            try:
                self.load_extension(cog)
            except Exception as e:
                traceback.print_exc()

    async def on_ready(self):
        print("I'm ready !")

def main():
    base = os.path.dirname(os.path.abspath(__file__))
    conf_path = os.path.normpath(os.path.join(base))
    conf = configparser.ConfigParser()
    conf.read(conf_path+'/config.ini', encoding='utf-8')
    client = MyBot(command_prefix='$')
    client.run(conf['DEFAULT']['BOT_TOKEN'])

if __name__ == '__main__':
    main()
