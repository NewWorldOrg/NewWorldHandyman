import configparser
import os
import src.py_modules as mod

def main():

    base = os.path.dirname(os.path.abspath(__file__))
    conf_path = os.path.normpath(os.path.join(base))
    conf = configparser.ConfigParser()
    conf.read(conf_path+'/config.ini', encoding='utf-8')
    client = mod.DiscordClient()
    client.run(conf['DEFAULT']['BOT_TOKEN'])

if __name__ == '__main__':
    main()
