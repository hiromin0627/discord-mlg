#coding: utf-8
#created by @hiromin0627

import discord
import asyncio
import configparser

ini = configparser.ConfigParser()
ini.read('./config.ini', 'UTF-8')

token = ini['tokens']['token-bgm']
vc_id = int(ini['ids']['vc'])

client = discord.Client()
channel = client.get_channel(vc_id)

@client.event
async def on_ready():
    print('---BGM player for MLG v1.0.0---')
    print('discord.py ver:' + discord.__version__)
    print('Logged in as ' + client.user.name + '(ID:' + str(client.user.id) + ')')
    print('Bot created by @hiromin0627')
    print('--------------------')

@client.event
async def on_message(message):
    if not message.author.bot:
        return

    if message.content.startswith("MLgacha"):
        vc = await channel.connect()
        vc.play(discord.FFmpegPCMAudio('./mlg/mlg_bgm.mp3'))
        while vc.is_playing():
            await asyncio.sleep(1)
            
    if message.content.startswith("disconnect"):
        if channel.is_connected():
            vc = channel.voice_client_in()
        else:
            vc = await channel.connect()
        await vc.disconnect()

client.run(token)