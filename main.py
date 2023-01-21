import signal
import json
import pyautogui
import argparse
import sys
import discord
from discord.ext import commands
from subprocess import Popen, CREATE_NEW_PROCESS_GROUP, DETACHED_PROCESS


with open('config.json', 'r') as config_file:
    config = json.load(config_file)
bot = commands.Bot(command_prefix=config['prefix'])


@bot.command(name='screenshot', help='Take a screenshot of the screen')
async def on_message(message):
    if message.author != bot.user:
        screenshot = pyautogui.screenshot()
        time = pyautogui.time.strftime('%Y-%m-%d_%H-%M-%S', pyautogui.time.localtime())
        name = f'images/screenshots/{time}.png'
        screenshot.save(name)
        await message.reply(file=discord.File(name))


@bot.command(name='stop', help='Stop the bot')
async def on_message(message):
    if message.author != bot.user:
        await bot.logout()


signal.signal(signal.SIGINT, signal.SIG_DFL)
parser = argparse.ArgumentParser(
    description='Discord bot that can take screenshots and stop itself',
    usage='%(prog)s -t TOKEN [options]'
)
parser.add_argument('-t', '--token', help='The bot token')
parser.add_argument('-d', '--detach', help='Detach the bot from the terminal', action='store_true')
args = parser.parse_args()


def main():
    bot.run(args.token)


if __name__ == '__main__':
    if args.token is None:
        print('Please provide a token\n')
        parser.print_help()
        exit(1)
    if args.detach:
        Popen([sys.executable, 'main.py', '-t', args.token], shell=False, creationflags=DETACHED_PROCESS | CREATE_NEW_PROCESS_GROUP)
    else:
        main()
