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

    if message.content.startswith("MLGstart"):
        channel = client.get_channel(vc_id)
        vc = await channel.connect()
        vc.play(discord.FFmpegPCMAudio('./resources/mlg_bgm.mp3'))
        while vc.is_playing():
            await asyncio.sleep(1)
            
    if message.content.startswith("disconnect"):
        try:
            if client.voice_clients[0] is not None:
                vc = client.voice_clients[0]
                await vc.disconnect()
        except:
            msg = await message.channel.send('BGM側ボットでエラーが発生しました')
            await asyncio.sleep(10)
            await msg.delete()

client.run(token)