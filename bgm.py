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
    print('---BGM player for MLG v1.1.0---')
    print('discord.py ver:' + discord.__version__)
    print('Logged in as ' + client.user.name + '(ID:' + str(client.user.id) + ')')
    print('Bot created by @hiromin0627')
    print('--------------------')

@client.event
async def on_message(message):
    if not message.author.bot:
        return

    if message.content.startswith("ML"):
        channel = client.get_channel(int(message.content[2:]))
        vc = await channel.connect()
        print('connected')
        vc.play(discord.FFmpegPCMAudio('./resources/mlg_bgm.mp3'))
        while True:
            target_reaction, user = await client.wait_for('reaction_add')
            if target_reaction.emoji == '⏹':
                await vc.disconnect()
                print('disconnected')
        while vc.is_connected():
            await asyncio.sleep(1)

client.run(token)