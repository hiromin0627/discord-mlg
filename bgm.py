#coding: utf-8
#created by @hiromin0627

import discord
import asyncio
import configparser

ini = configparser.ConfigParser()
ini.read('./config.ini', 'UTF-8')

token = ini['tokens']['token-bgm']

client = discord.Client()

@client.event
async def on_ready():
    print('---BGM player for MLG v1.2.0---')
    print('discord.py ver:' + discord.__version__)
    print('Logged in as ' + client.user.name + '(ID:' + str(client.user.id) + ')')
    print('Bot created by @hiromin0627')
    print('--------------------')

@client.event
async def on_message(message):
    if not message.author.bot:
        return

    if message.content.startswith("ML") and not message.content[2:] == '' and is_int(message.content[2:]):
        channel = client.get_channel(int(message.content[2:]))
        vc = await channel.connect()
        print('connected')
        vc.play(discord.FFmpegPCMAudio('./resources/mlg_bgm.mp3'))
        while True:
            target_reaction, user = await client.wait_for('reaction_add')
            if target_reaction.emoji == '⏹' and user == message.author:
                await vc.disconnect()
                print('disconnected')
                break

def is_int(s):
  try:
    int(s)
  except:
    return False
  return True

client.run(token)