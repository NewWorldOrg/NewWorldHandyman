from discord.ext import commands
from dotenv import load_dotenv
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
    base_path = os.path.dirname(os.path.abspath(__file__))
    dotenv_path = os.path.join(base_path, '.env')
    load_dotenv(dotenv_path)

    client = MyBot(command_prefix='$')
    client.run(os.getenv('BOT_TOKEN'))

if __name__ == '__main__':
    main()
