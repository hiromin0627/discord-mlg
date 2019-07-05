#coding: utf-8
#created by @hiromin0627
 
import discord
import asyncio
import re,random
import datetime
import csv
from threading import (Event, Thread)
from urllib import request
import configparser

import imas

ini = configparser.ConfigParser()
ini.read('./config.ini', 'UTF-8')

token = ini['tokens']['token']

vc_id = int(ini['ids']['vc'])
bgm_id = int(ini['ids']['bgm-room'])
log_id = int(ini['ids']['log-room'])

prefix = ini['Prefix']['commandprefix']

timeout = float(ini['Reaction']['timeout'])

client = discord.Client()

pickup_name = ''
rider_flag = 0
feslist = list()
ssrlist = list()
srlist = list()
rlist = list()
mlg_all = list()
pickup = list()

@client.event
async def on_ready():
    print('---MilliShita Gacha 1.0.0 Alpha---')
    print('discord.py ver:' + discord.__version__)
    print('Logged in as ' + client.user.name + '(ID:' + str(client.user.id) + ')')
    print('Bot created by @hiromin0627')
    print('--------------------')
    print('Loading mlg lists...')
    await gacha_reload()
    print('mlg lists loaded.')
    print('--------------------')

@client.event
async def on_message(message):
    if message.author.bot:
        return

    if message.content.startswith("MLhelp"):
        await message.delete()
        print('Start MLhelp')
        msg = await message.channel.send('ミリシタガシャシミュレーターDiscordボット v0.1.0\n' +\
            prefix + 'help：ヘルプコマンドです。ミリシタガシャの説明を見ることができます。\n' +\
            prefix + 'reload：ミリシタガシャデータベースをダウンロードして更新します。\n' +\
            prefix + 'cards：MLガシャで引いたカード名を確認することができます。\n' +\
            prefix + 'pickup：現在のガシャ名とピックアップカードを確認できます。\n' +\
            prefix + 'call：MLガシャで引いたカード画像を検索できます。スペースを挟んでカード名を入力してください。（制服シリーズはアイドル名も記入）\n' +\
            prefix + 'ガシャ：ミリシタガシャシミュレーターができます。10を後に入力すると、10連ガシャになります。')
        print('MLhelp complite.')
    elif message.content.startswith(prefix + "reload"):
        await message.delete()
        print('Start MLreload')
        await gacha_reload()
        print('MLreload complite.')
        msgn = await message.channel.send('MLreload complite.')
        await asyncio.sleep(10)
        await msgn.delete()
    elif message.content.startswith(prefix + 'cards'):
        await message.delete()
        print('Start MLGacha[cards].')
        await gacha_note(message)
    elif message.content.startswith(prefix + 'pickup'):
        await message.delete()
        print('Start MLGacha[pickup].')
        name = ''
        for val in pickup:
            if val[5] == 3:
                ra = '［FES］'
            elif val[5] == 2 and val[6] == 3:
                ra = '［限定SSR］'
            elif val[5] == 2 and val[6] == 2:
                ra = '［SSR］'
            elif val[5] == 1 and val[6] == 3:
                ra = '［限定SR］'
            elif val[5] == 1 and val[6] == 2:
                ra = '［SR］'
            elif val[5] == 0:
                ra = '［R］'
            name += ra + val[1] + ' ' + val[0] + '\n'

        emb = discord.Embed(title='現在のミリシタガシャピックアップはこちらです！！', description=name)
        emb.set_author(name=pickup_name)
        await message.channel.send('', embed=emb)
    elif message.content.startswith(prefix + 'call'):
        await message.delete()
        print('Start MLGacha[call].')
        cv = ''
        desc = ''
        char_list = list()
        carddata = []
        rear = ''

        try:
            with open('./gacha/' + str(message.author.id) + '.txt', 'r') as f:
                listline = f.read()
                char_list = list(listline)
        except:
            pass

        if '制服シリーズ' in message.content[6:]:
            for data in imas.million_data:
                if data[0] in message.content[6:]:
                    for r,val in enumerate(mlg_all):
                        if val[0] in message.content[6:] and val[1] == '制服シリーズ':
                            if char_list[r] == '1':
                                carddata = val
            if len(carddata) == 0:
                msgn = await message.channel.send('制服シリーズの場合、アイドル名も同時に入力する必要があります。')
                await asyncio.sleep(10)
                await msgn.delete()
                return
        else:
            for r,val in enumerate(mlg_all):
                if val[1] in message.content[6:]:
                    if char_list[r] == '1':
                        carddata = val

        if len(carddata) == 0:
            msgn = await message.channel.send('カード名が違うか、このカードを所持していません！\n「MLcheck」で自分が所持しているカード名を確認してください。')
            await asyncio.sleep(10)
            await msgn.delete()
            return

        for r,data in enumerate(imas.million_data):
            if carddata[0] in data[0]:
                cv = 'CV.' + data[3]
                color = data[2]
        if carddata[5] == '3':
            rear = 'FES'
        elif carddata[5] == '2':
            rear = 'SSR'
        elif carddata[5] == '1':
            rear = 'SR'
        elif carddata[5] == '0':
            rear = 'R'

        desc = rear + carddata[1] + ' ' + carddata[0]
        embmsg1 = discord.Embed(title=desc, description=cv, colour=color)
        embmsg1.set_author(name=message.author.name + 'の所持カード', icon_url=message.author.avatar_url)
        embmsg1.set_image(url=carddata[2])
        if carddata[5] >= 2:
            msg = await message.channel.send('👆を押して覚醒後へ', embed=embmsg1)
        else:
            msg = await message.channel.send('👆を押して閉じる', embed=embmsg1)
        await msg.add_reaction('👆')
        while True:
            target_reaction, user = await client.wait_for('reaction_add')
            if target_reaction.emoji == '👆' and user != msg.author:
                if carddata[5] == 2 or carddata[5] == 3:
                    await msg.remove_reaction(target_reaction.emoji, user)
                    embmsg1.set_image(url=carddata[3])
                    await msg.edit(content='👆を押して閉じる', embed=embmsg1)
                    while True:
                        target_reaction, user = await client.wait_for('reaction_add')
                        if target_reaction.emoji == '👆' and user != msg.author:
                            await msg.delete()
                            return
                else:
                    target_reaction, user = await client.wait_for('reaction_add')
                    if target_reaction.emoji == '👆' and user != msg.author:
                        await msg.delete()
                        return
                return
    elif message.content.startswith(prefix + "ガシャ"):
        await message.delete()
        kind = ''
        result = []
        img = ''
        author = message.author
        
        channel = client.get_channel(vc_id)
        
        gacha_count = int()

        try:
            with open('./gacha_count/' + str(author.id) + '.txt', 'r') as f:
                gacha_count = int(f.read())
        except:
            with open('./gacha_count/' + str(author.id) + '.txt', 'w') as f:
                f.write('0')

        if gacha_count >= 300:
            count_emoji = ['1⃣','2⃣','3⃣','4⃣','5⃣','6⃣','7⃣','8⃣','9⃣','🔟']
            pickup_counter = 0
            pickup_alllist = list()
            name = ''
            for val in pickup:
                if val[5] == 2 and val[6] == 3:
                    ra = '［限定SSR］'
                elif val[5] >= 2:
                    ra = '［SSR］'
                elif val[5] == 1 and val[6] == 3:
                    ra = '［限定SR］'
                elif val[5] == 1:
                    ra = '［SR］'
                elif val[5] == 0:
                    ra = '［R］'
                pickup_alllist.append(val)
                name += count_emoji[pickup_counter] + '　' + ra + val[1] + ' ' + val[0] + '\n'
                pickup_counter += 1

            mlgpickupemb = discord.Embed(title='交換カード一覧', description=name)
            mlgpickupemb.set_author(name=author.name, icon_url=author.avatar_url)
            mlgpickupemb.set_footer(text=pickup_name)
            msgs = await message.channel.send('ドリームスターがカード交換数に達しているため、ガシャをご利用いただけません。カードを交換してください。\n該当番号のリアクションを返すと交換できます。', embed=mlgpickupemb)

            for r in range(pickup_counter):
                await msgs.add_reaction(count_emoji[r])

            kind = 'ドリームスター交換「' + pickup_name + '」'
            try:
                gacha_count = 0
                with open('./gacha_count/' + str(author.id) + '.txt', 'w') as f:
                    f.write(str(gacha_count))
            except:
                print('Gacha count FAILED.')

            pickup_num = int()
            while True:
                target_reaction, user = await client.wait_for('reaction_add')
                if not user == msgs.author:
                    if target_reaction.emoji == '1⃣':
                        pickup_num = 0
                        break
                    elif target_reaction.emoji == '2⃣':
                        pickup_num = 1
                        break
                    elif target_reaction.emoji == '3⃣':
                        pickup_num = 2
                        break
                    elif target_reaction.emoji == '4⃣':
                        pickup_num = 3
                        break
                    elif target_reaction.emoji == '5⃣':
                        pickup_num = 4
                        break
                    elif target_reaction.emoji == '6⃣':
                        pickup_num = 5
                        break
                    elif target_reaction.emoji == '7⃣':
                        pickup_num = 6
                        break
                    elif target_reaction.emoji == '8⃣':
                        pickup_num = 7
                        break
                    elif target_reaction.emoji == '9⃣':
                        pickup_num = 8
                        break
                    elif target_reaction.emoji == '🔟':
                        pickup_num = 9
                        break

            result = pickup_alllist[pickup_num]

            if result[5] >= 2:
                img = 'https://i.imgur.com/jWTTZ0d.gifv'
            elif result[5] == 1:
                img = 'https://i.imgur.com/vF7fDn3.gifv'
            else:
                img = 'https://i.imgur.com/hEHa49X.gifv'

            await msgs.delete()

            print('Start MLChange[' + kind + '] by ' + str(author.id) + '.')

            if not 'SILENT' in message.content.upper() or 'サイレント' in message.content:
                vc = await channel.connect()
                if not bgm_id == 0:
                    toBot = client.get_channel(bgm_id)
                    await toBot.send('MLgacha')

            await asyncio.sleep(0.7)
            msg = await message.channel.send(author.mention + ' https://i.imgur.com/da2w9YS.gifv')
            await msg.add_reaction('👆')

            await mlg_touch(msg,message,result,img,author,kind,vc,20,0)

            if vc.is_connected():
                while vc.is_playing():
                    await asyncio.sleep(2)
            return

        role = 0

        fes_flag = 0
        ssr_flag = 0
        sr_flag = 0

        if '10' in message.content or '１０' in message.content:
            role = 10
        else:
            role = 1

        try:
            gacha_count += role
            with open('./gacha_count/' + str(author.id) + '.txt', 'w') as f:
                f.write(str(gacha_count))
        except:
            print('ガシャ回数の記録ができませんでした。')

        kind = str(role) + '回プラチナガシャ「' + pickup_name + '」'
        
        for n in range(role):
            if n < 9:
                rand = random.randint(1, 100)
                if pickup_name == 'ミリオンフェス':
                    if rand >= 1 and rand <= 6:
                        result.append(ssrlist[random.randrange(len(ssrlist) - 1)])
                        ssr_flag = 1
                    elif rand >= 7 and rand <= 18:
                        result.append(srlist[random.randrange(len(srlist) - 1)])
                        sr_flag = 1
                    elif rand >= 18 and rand <= 100:
                        result.append(rlist[random.randrange(len(rlist) - 1)])
                else:
                    if rand >= 1 and rand <= 3:
                        result.append(ssrlist[random.randrange(len(ssrlist) - 1)])
                        ssr_flag = 1
                    elif rand >= 4 and rand <= 15:
                        result.append(srlist[random.randrange(len(srlist) - 1)])
                        sr_flag = 1
                    elif rand >= 16 and rand <= 100:
                        result.append(rlist[random.randrange(len(rlist) - 1)])
            if n == 9:
                if pickup_name == 'ミリオンフェス':
                    rand = random.randint(1, 100)
                    if rand >= 1 and rand <= 6:
                        result.append(ssrlist[random.randrange(len(ssrlist) - 1)])
                        ssr_flag = 1
                    elif rand >= 7 and rand <= 100:
                        result.append(srlist[random.randrange(len(srlist) - 1)])
                        sr_flag = 1
                else:
                    rand = random.randint(1, 100)
                    if rand >= 1 and rand <= 3:
                        result.append(ssrlist[random.randrange(len(ssrlist) - 1)])
                        ssr_flag = 1
                    elif rand >= 4 and rand <= 100:
                        result.append(srlist[random.randrange(len(srlist) - 1)])
                        sr_flag = 1

        if pickup_name == 'ミリオンフェス':
            for val in result:
                if val[5] == 3:
                    fes_flag = 1

        pink_flag = random.randint(1, 20)
        if fes_flag == 1:
            if pink_flag == 10:
                img = 'https://i.imgur.com/fGpfCgB.gifv'
            elif pink_flag == 20:
                img = 'https://i.imgur.com/jWTTZ0d.gifv'
            else:
                img = 'https://i.imgur.com/0DxyVhm.gifv'
        elif ssr_flag == 1 and not fes_flag == 1:
            img = 'https://i.imgur.com/jWTTZ0d.gifv'
        elif sr_flag == 1 and not fes_flag == 1 and not ssr_flag == 1:
            img = 'https://i.imgur.com/vF7fDn3.gifv'
        else:
            img = 'https://i.imgur.com/hEHa49X.gifv'

        if not 'SILENT' in message.content.upper() or 'サイレント' in message.content:
            vc = await channel.connect()
        print('Start MLGacha[' + kind + '] by ' + author.name + '.')

        mess = random.randint(1,10)
        phrase = str()
        if mess >= 2 and (ssr_flag == 1 or fes_flag == 1):
            phrase = '最高の一枚ができましたのでぜひご確認ください！'
        elif mess <= 4 and (sr_flag == 1 or ssr_flag == 1 or fes_flag == 1):
            phrase = 'みんなのいい表情が撮れました！'
        elif mess > 4 and mess <= 8 and (sr_flag == 1 or ssr_flag == 1 or fes_flag == 1):
            phrase = '楽しそうなところが撮れましたよ'

        if not len(phrase) == 0:
            vc.play(discord.FFmpegPCMAudio('./resources/message.mp3'))
            camera = await message.channel.send(phrase)
            while vc.is_playing():
                await asyncio.sleep(3)
            await camera.delete()

        if not 'SILENT' in message.content.upper() or 'サイレント' in message.content:
            if not bgm_id == 0:
                toBot = client.get_channel(bgm_id)
                await toBot.send('MLgacha')

        await asyncio.sleep(0.7)
        if fes_flag == 1 and pink_flag == 10:
            msg = await message.channel.send(author.mention + ' https://i.imgur.com/ZC8JK9i.gifv')
        else:
            msg = await message.channel.send(author.mention + ' https://i.imgur.com/da2w9YS.gifv')
        await msg.add_reaction('👆')

        await mlg_touch(msg,message,result,img,author,kind,vc,pink_flag,fes_flag)
            
        if vc.is_connected():
            while vc.is_playing():
                await asyncio.sleep(2)

async def gacha_reload():
    global mlg_all, feslist, ssrlist, srlist, rlist, pickup, pickup_name
    ssrlist = []
    srlist = []
    rlist = []
    feslist = []
    mlg_all = []
    pickup = []
    
    with open('./resources/pickup_name.txt',encoding="utf-8_sig") as f:
        pickup_name = f.read()

    fescount = 0
    ssrcount = 0
    srcount = 0
    rcount = 0
    with open('./resources/mlg_all.csv',encoding="utf-8_sig") as f:
        reader = csv.reader(f)
        for row in reader:
            indata = [row[3],str(row[4]),row[5],row[6],str(row[7]),int(row[2]),int(row[1]),int(row[0])]
            mlg_all.insert(0, indata)
            fesmode = 0

            if indata[5] == 3:
                feslist.insert(0, indata)
                fescount += 1
                if indata[6] >= 2:
                    fesmode = 1
                    for n in range(15):
                        ssrlist.insert(0, indata)
            elif indata[5] == 2 and not int(row[1]) == 0:
                ssrlist.insert(0, indata)
                ssrcount += 1
                if indata[6] >= 2:
                    for n in range(19):
                        ssrlist.insert(0, indata)
            elif indata[5] == 1 and not int(row[1]) == 0:
                srlist.insert(0, indata)
                srcount += 1
                if indata[6] >= 2:
                    for n in range(19):
                        srlist.insert(0, indata)
            elif indata[5] == 0:
                rlist.insert(0, indata)
                rcount += 1
                if indata[6] >= 2:
                    for n in range(7):
                        rlist.insert(0, indata)

    for row in mlg_all:
        if row[6] >= 2 and row[5] >= 2:
            pickup.append(row)
    for row in mlg_all:
        if row[6] >= 2 and row[5] == 1:
            pickup.append(row)
    for row in mlg_all:
        if row[6] >= 2 and row[5] == 0:
            pickup.append(row)
            
    print('Loaded ' + str(len(mlg_all)) + 'cards.')
    if fesmode == 0:
        fescount = 0
    elif fesmode == 1:
        print(str(fescount) + ' FESCards available. ')
    print(str(ssrcount) + ' SSRCards available.')
    print(str(srcount) + ' SRCards available.')
    print(str(rcount) + ' RCards available.')
    print('Available ' + str(fescount + ssrcount + srcount + rcount) + ' cards.')
    print('Pickup name is 「' + pickup_name + '」')
    print('Pickup cards')
    for row in pickup:
        if row[6] == 3:
            print(str(row[5]) + ' ' + row[1] + ' ' + row[0] + ' [Limited card]')
        else:
            print(str(row[5]) + ' ' + row[1] + ' ' + row[0])
    return

async def gacha_note(message):
    char_list = list()
    try:
        with open('./gacha/' + str(message.author.id) + '.txt', 'r') as f:
            listline = f.read()
            char_list = list(listline)
    except:
        import traceback
        traceback.print_exc()
        await message.channel.send(message.author.mention + 'の所持SSRの記録がないか、エラーが発生しました。')
        return

    text = ['']
    cards = []
    page = 0
    count = 0

    for n in range(4):
        for val in mlg_all:
            try:
                if char_list[val[7]] == '1' and val[5] == n:
                    cards.insert(0, val)
            except:
                pass

    for val in cards:
        count += 1
        if count == 10:
            text.append('')
            page += 1
            count = 0

        if val[5] == 2:
            rarity = '［SSR］'
        elif val[5] == 3:
            rarity = '［FES］'
        elif val[5] == 1:
            rarity = '［SR］'
        elif val[5] == 0:
            rarity = '［R］'
        text[page] += '\n' + rarity + val[1] + ' ' + val[0]

    gacha_count = str()
    try:
        with open('./gacha_count/' + str(message.author.id) + '.txt', 'r') as f:
            gacha_count = f.read()
    except:
        pass

    fotter_text = 'ドリームスター所持数：' + gacha_count

    now = 1

    emb = discord.Embed(title='所持SSR一覧 Page ' + str(now) + '/' + str(len(text)), description=text[now - 1])
    emb.set_author(name=message.author.name, icon_url=message.author.avatar_url)
    emb.set_footer(text=fotter_text)
    msg = await message.channel.send('見終わったら❌で消してね！', embed=emb)
    await msg.add_reaction('◀')
    await msg.add_reaction('▶')
    await msg.add_reaction('❌')

    while True:
        try:
            target_reaction, user = await client.wait_for('reaction_add', timeout=timeout)

            if target_reaction.emoji == '◀' and user != msg.author:
                if not now == 1:
                    now -= 1
                    emb = discord.Embed(title='所持カード一覧 Page ' + str(now) + '/' + str(len(text)), description=text[now - 1])
                    emb.set_author(name=message.author.name, icon_url=message.author.avatar_url)
                    emb.set_footer(text=fotter_text)
                    await msg.edit(embed=emb)
                else:
                    now = len(text)
                    emb = discord.Embed(title='所持カード一覧 Page ' + str(now) + '/' + str(len(text)), description=text[now - 1])
                    emb.set_author(name=message.author.name, icon_url=message.author.avatar_url)
                    emb.set_footer(text=fotter_text)
                    await msg.edit(embed=emb)
                await msg.remove_reaction(target_reaction.emoji, user)
            elif target_reaction.emoji == '▶' and user != msg.author:
                if not now == len(text):
                    now += 1
                    emb = discord.Embed(title='所持カード一覧 Page ' + str(now) + '/' + str(len(text)), description=text[now - 1])
                    emb.set_author(name=message.author.name, icon_url=message.author.avatar_url)
                    emb.set_footer(text=fotter_text)
                    await msg.edit(embed=emb)
                else:
                    now = 1
                    emb = discord.Embed(title='所持カード一覧 Page ' + str(now) + '/' + str(len(text)), description=text[now - 1])
                    emb.set_author(name=message.author.name, icon_url=message.author.avatar_url)
                    emb.set_footer(text=fotter_text)
                    await msg.edit(embed=emb)
                await msg.remove_reaction(target_reaction, user)
            elif target_reaction.emoji == '❌' and user != msg.author:
                await msg.delete()
                break
            else:
                pass
        except asyncio.TimeoutError:
            await msg.edit(content='しばらく操作がなかったため、タイムアウトしました。',embed=None)
            await asyncio.sleep(10)
            await msg.delete()
            break

async def mlg_touch(msg,message,result,img,author,kind,vc,pink_flag,fes_flag):
    try:
        rarity = ''
        log = ''
        count = 0
        while True:
            target_reaction, user = await client.wait_for('reaction_add', timeout=timeout)
            if user == author and target_reaction.emoji == '👆':
                await msg.clear_reactions()
                await msg.edit(content=img)

                if vc.is_connected():
                    await asyncio.sleep(0.4)
                    if fes_flag == 1 and not pink_flag == 20:
                        vc.play(discord.FFmpegPCMAudio('./resources/open_fes.mp3'))
                    else:
                        vc.play(discord.FFmpegPCMAudio('./resources/open.mp3'))
                    while vc.is_playing():
                        await asyncio.sleep(1)
                break

        while count < len(result):
            result_10 = result[count]
            if result_10[5] == 3:
                rarity = 'FES SSR'
                player_show = discord.FFmpegPCMAudio('./resources/fes.mp3')
                await msg.clear_reactions()
            elif result_10[5] == 2:
                rarity = 'SSR'
                player_show = discord.FFmpegPCMAudio('./resources/ssr.mp3')
                await msg.clear_reactions()
            elif result_10[5] == 1:
                rarity = 'SR'
                player_show = discord.FFmpegPCMAudio('./resources/normal.mp3')
            elif result_10[5] == 0:
                rarity = 'R'
                player_show = discord.FFmpegPCMAudio('./resources/normal.mp3')

            desc = rarity + '　' + result_10[1] + '　' + result_10[0]
            for data in imas.million_data:
                if result_10[0] in data[0]:
                    color = data[2]
                    cv = 'CV.' + data[3]
            mlgnormalemb = discord.Embed(title=desc, description=cv, colour=color)

            footer_text = kind + str((count + 1)) + '枚目'
            mlgnormalemb.set_author(name=author.name, icon_url=author.avatar_url)
            mlgnormalemb.set_footer(text=footer_text)

            mlgnormalemb.set_image(url=result_10[2])
            if vc.is_connected():
                vc.play(player_show)

            #カード表示（SSRの場合特訓前）
            await msg.edit(content=author.mention, embed=mlgnormalemb)

            char_list = list()

            try:
                with open('./gacha/' + str(author.id) + '.txt', 'r') as f:
                    listline = f.read()
                    char_list = list(listline)
            except:
                pass

            with open('./gacha/' + str(author.id) + '.txt', 'w+') as f:
                try:
                    char_list[result_10[7]] = '1'
                except:
                    for n in range(500):
                        char_list.append('0')
                    char_list[result_10[7]] = '1'

                newlistline = ''.join(char_list)
                f.write(newlistline)

            if rarity == 'SSR' or rarity == 'FES SSR':
                if vc.is_connected():
                    while vc.is_playing():
                        await asyncio.sleep(1)
                    vc.play(discord.FFmpegPCMAudio('./resources/ssr_talk.mp3'))

                line = result_10[4].replace("ProP", author.name + "P")
                mlgssremb = discord.Embed(title=desc, description=cv, colour=color)
                mlgssremb.set_footer(text=footer_text, icon_url=author.avatar_url)
                mlgssremb.set_image(url=result_10[3])

                await asyncio.sleep(4.2)
                await msg.edit(content=author.mention, embed=mlgssremb)
                await asyncio.sleep(3)
                await msg.edit(content=author.mention + ' ' + result_10[0] + '「' + line + '」', embed=mlgssremb)

            await msg.add_reaction('👆')
            await msg.add_reaction('⏭')
            while True:
                target_reaction2, user = await client.wait_for('reaction_add', timeout=timeout)

                if target_reaction2.emoji == '👆' and user == author:
                    if vc.is_connected():
                        if vc.is_playing():
                            vc.stop()
                    count += 1
                    log += '[' + rarity + ']' + result_10[1] + ' ' + result_10[0] + '\n'
                    if count == len(result):
                        if vc.is_connected():
                            if not bgm_id == 0:
                                toBot = client.get_channel(bgm_id)
                                await toBot.send('disconnect')
                        await vc.disconnect()
                        await msg.clear_reactions()
                        await msg.delete()

                        gacha_count = str()
                        try:
                            with open('./gacha_count/' + str(message.author.id) + '.txt', 'r') as f:
                                gacha_count = f.read()
                        except:
                            print('Gacha count read FAILED.')

                        toLog = client.get_channel(log_id)
                        footer_text = kind
                        mlglogemb = discord.Embed(title='ガシャ結果', description=log + '\nドリームスター所持数：' + gacha_count)
                        mlglogemb.set_author(name=author.name, icon_url=author.avatar_url)
                        mlglogemb.set_footer(text=footer_text)
                        await toLog.send(embed=mlglogemb)

                        return
                    else:
                        await msg.remove_reaction(target_reaction2.emoji, user)
                    break
                elif target_reaction2.emoji == '⏭' and user == author:
                    if vc.is_connected():
                        if not bgm_id == 0:
                            toBot = client.get_channel(bgm_id)
                            await toBot.send('disconnect')
                        await vc.disconnect()

                    for n,box in enumerate(result):
                        if count > n:
                            continue

                        if box[5] == 3:
                            rarity = 'FES SSR'
                        elif box[5] == 2:
                            rarity = 'SSR'
                        elif box[5] == 1:
                            rarity = 'SR'
                        elif box[5] == 0:
                            rarity = 'R'
                        log += '[' + rarity + ']' + box[1] + ' ' + box[0] + '\n'

                        char_list = list()

                        try:
                            with open('./gacha/' + str(author.id) + '.txt', 'r') as f:
                                listline = f.read()
                                char_list = list(listline)
                        except:
                            pass

                        with open('./gacha/' + str(author.id) + '.txt', 'w+') as f:
                            try:
                                char_list[box[7]] = '1'
                            except:
                                for n in range(500):
                                    char_list.append('0')
                                char_list[box[7]] = '1'

                            newlistline = ''.join(char_list)
                            f.write(newlistline)

                    gacha_count = str()
                    try:
                        with open('./gacha_count/' + str(message.author.id) + '.txt', 'r') as f:
                            gacha_count = f.read()
                    except:
                        print('Gacha count FAILED.')

                    count += 10
                    await msg.delete()
                    toLog = client.get_channel(log_id)
                    footer_text = kind
                    mlglogemb = discord.Embed(title='ガシャ結果', description=log + '\nドリームスター所持数：' + gacha_count)
                    mlglogemb.set_author(name=author.name, icon_url=author.avatar_url)
                    mlglogemb.set_footer(text=footer_text)
                    await toLog.send(embed=mlglogemb)
                    break
        print('MLGacha complete. ' + author.name + '`s result\n' + log)
    except TimeoutError:
        await msg.delete()
        if vc.is_connected():
            await vc.disconnect()
        if not bgm_id == 0:
            toBot = client.get_channel(bgm_id)
            await toBot.send('disconnect')
        await message.channel.send('タイムアウトしました。')
    """ except:
        import traceback
        traceback.print_exc()
        await msg.delete()
        if vc.is_connected():
            await vc.disconnect()
        if not bgm_id == 0:
            toBot = client.get_channel(bgm_id)
            await toBot.send('disconnect') """

client.run(token)