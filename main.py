#coding: utf-8
#created by @hiromin0627
#MilliShita Gacha 1.1.0

import glob
import gettext
import os
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

lang = ini['Language']['lang']

path_to_locale_dir = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        './locale'
    )
)
if lang == 'cn': translang = 'zh_TW'
elif lang == 'kr': translang = 'ko_KR'
else: translang = 'ja_JP'
translater = gettext.translation('messages',localedir=path_to_locale_dir,languages=[translang],fallback=True,codeset="utf8")
translater.install()

token = ini['tokens']['token']

vc_id = int(ini['ids']['vc'])
bgm_id = int(ini['ids']['bgm-room'])
log_id = int(ini['ids']['log-room'])

prefix = ini['Prefix']['commandprefix']

timeout = float(ini['Reaction']['timeout'])

client = discord.Client()

pickup_name = ''
feslist = list()
ssrlist = list()
srlist = list()
rlist = list()
mlg_all = list()
ssrpicklist = list()
srpicklist = list()
rpicklist = list()
rarity_str = ['R','SR','SSR','FES']

timer = 0

@client.event
async def on_ready():
    print('---MilliShita Gacha 1.0.0---')
    print('discord.py ver:' + discord.__version__)
    print('Logged in as ' + client.user.name + '(ID:' + str(client.user.id) + ')')
    print('Bot created by @hiromin0627')
    await gacha_reload(0,None)

@client.event
async def on_message(message):
    if message.author.bot:
        return

    if message.content.startswith("MLhelp"):
        await message.delete()
        print('Start MLhelp')
        if lang == 'ja':
            msg = await message.channel.send('ミリシタガシャシミュレーターDiscordボット v1.1.0\n' +\
                prefix + 'help：ヘルプコマンドです。ミリシタガシャの説明を見ることができます。\n' +\
                prefix + 'reload：ミリシタガシャデータベースをダウンロードして更新します。\n' +\
                prefix + 'reset：全ユーザーのMLガシャを引いた回数をリセットします。\n' +\
                prefix + 'cards：MLガシャで引いたカード名を確認することができます。\n' +\
                prefix + 'pickup：現在のガシャ名とピックアップカードを確認できます。\n' +\
                prefix + 'call：MLガシャで引いたカード画像を検索できます。スペースを挟んでカード名を入力してください。（制服シリーズはアイドル名も記入）\n' +\
                prefix + 'ガシャ or ' + prefix + 'gacha：ミリシタガシャシミュレーターができます。10を後に入力すると、10連ガシャになります。')
        elif lang == 'cn':
            msg = await message.channel.send('劇場時光轉蛋模擬器Discord Bot v1.1.0\n' +\
                prefix + 'help：ヘルプコマンドです。ミリシタガシャの説明を見ることができます。\n' +\
                prefix + 'reload：ミリシタガシャデータベースをダウンロードして更新します。\n' +\
                prefix + 'reset：全ユーザーのMLガシャを引いた回数をリセットします。\n' +\
                prefix + 'cards：MLガシャで引いたカード名を確認することができます。\n' +\
                prefix + 'pickup：現在のガシャ名とピックアップカードを確認できます。\n' +\
                prefix + 'call：MLガシャで引いたカード画像を検索できます。スペースを挟んでカード名を入力してください。（制服シリーズはアイドル名も記入）\n' +\
                prefix + '轉蛋 or ' + prefix + 'gacha：ミリシタガシャシミュレーターができます。10を後に入力すると、10連ガシャになります。')
        elif lang == 'kr':
            msg = await message.channel.send('밀리언 라이브! 시어터 데이즈 촬영 시뮬레이터 Discord Bot v1.1.0\n' +\
                prefix + 'help：ヘルプコマンドです。ミリシタガシャの説明を見ることができます。\n' +\
                prefix + 'reload：ミリシタガシャデータベースをダウンロードして更新します。\n' +\
                prefix + 'reset：全ユーザーのMLガシャを引いた回数をリセットします。\n' +\
                prefix + 'cards：MLガシャで引いたカード名を確認することができます。\n' +\
                prefix + 'pickup：現在のガシャ名とピックアップカードを確認できます。\n' +\
                prefix + 'call：MLガシャで引いたカード画像を検索できます。スペースを挟んでカード名を入力してください。（制服シリーズはアイドル名も記入）\n' +\
                prefix + '촬영 or ' + prefix + 'gacha：ミリシタガシャシミュレーターができます。10を後に入力すると、10連ガシャになります。')
        else:
            msg = await message.channel.send('Million Live! Theater Days Gacha Simulator Discord Bot v1.1.0\n' +\
                prefix + 'help：ヘルプコマンドです。ミリシタガシャの説明を見ることができます。\n' +\
                prefix + 'reload：ミリシタガシャデータベースをダウンロードして更新します。\n' +\
                prefix + 'reset：全ユーザーのMLガシャを引いた回数をリセットします。\n' +\
                prefix + 'cards：MLガシャで引いたカード名を確認することができます。\n' +\
                prefix + 'pickup：現在のガシャ名とピックアップカードを確認できます。\n' +\
                prefix + 'call：MLガシャで引いたカード画像を検索できます。スペースを挟んでカード名を入力してください。（制服シリーズはアイドル名も記入）\n' +\
                prefix + 'ガシャ or ' + prefix + 'gacha：ミリシタガシャシミュレーターができます。10を後に入力すると、10連ガシャになります。')
        
        print('MLhelp complite.')
    elif message.content.startswith(prefix + "reload"):
        await message.delete()
        if timer > 0:
            msgn = await message.channel.send(_('リロード直後です。') + str(timer) + _('秒後にお試しください。'))
            await asyncio.sleep(10)
            await msgn.delete()
            return
        print('Start MLreload')
        await gacha_reload(1,message)
        print('MLreload complite.')
    elif message.content.startswith(prefix + 'cards'):
        await message.delete()
        print('Start MLGacha[cards].')
        await gacha_note(message)
    elif message.content.startswith(prefix + 'reset'):
        await message.delete()
        print('Start MLGacha[reset].')
        file_list = glob.glob("./gacha_count/*.txt")
        for file in file_list:
            os.remove(file)
        msgn = await message.channel.send(_('すべてのユーザーのガチャカウントをリセットしました。'))
        await asyncio.sleep(10)
        await msgn.delete()
    elif message.content.startswith(prefix + 'pickup'):
        await message.delete()
        print('Start MLGacha[pickup].')
        name = ''
        for val in pickup:
            lim = _('限定') if val[6] == 3 else ''
            name += '［' + lim + rarity_str[val[5]] + '］' + val[1] + ' ' + val[0] + '\n'

        emb = discord.Embed(title=_('現在のミリシタガシャピックアップはこちらです！！'), description=name)
        emb.set_author(name=pickup_name)
        await message.channel.send('', embed=emb)
    elif message.content.startswith(prefix + 'call'):
        await message.delete()
        print('Start MLGacha[call].')
        cv = ''
        desc = ''
        char_list = list()
        carddata = []

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
                msgn = await message.channel.send(_('制服シリーズの場合、アイドル名も同時に入力する必要があります。'))
                await asyncio.sleep(10)
                await msgn.delete()
                return
        else:
            for r,val in enumerate(mlg_all):
                if val[1] in message.content[6:]:
                    if char_list[r] == '1':
                        carddata = val

        if len(carddata) == 0:
            msgn = await message.channel.send(_('カード名が違うか、このカードを所持していません！\n「MLcheck」で自分が所持しているカード名を確認してください。'))
            await asyncio.sleep(10)
            await msgn.delete()
            return

        if lang == 'ja': lang_data = 0
        elif lang == 'cn': lang_data = 4
        elif lang == 'kr': lang_data = 6
        else: lang_data = 0
        for data in imas.million_data:
            if carddata[0] in data[lang_data]:
                color = data[3]
                cv = 'CV.' + data[lang_data + 1]

        desc = '[' + rarity_str[int(carddata[5])] + ']' + carddata[1] + ' ' + carddata[0]
        embmsg1 = discord.Embed(title=desc, description=cv, colour=color)
        embmsg1.set_author(name=message.author.name + _('所持カード'), icon_url=message.author.avatar_url)
        embmsg1.set_image(url=carddata[2])
        if carddata[5] >= 2:
            msg = await message.channel.send('👆' + _('を押して覚醒後へ'), embed=embmsg1)
        else:
            msg = await message.channel.send('👆' + _('を押して閉じる'), embed=embmsg1)
        await msg.add_reaction('👆')
        while True:
            target_reaction, user = await client.wait_for('reaction_add')
            if target_reaction.emoji == '👆' and user != msg.author:
                if carddata[5] == 2 or carddata[5] == 3:
                    await msg.remove_reaction(target_reaction.emoji, user)
                    embmsg1.set_image(url=carddata[3])
                    await msg.edit(content='👆' + _('を押して閉じる'), embed=embmsg1)
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
    elif message.content.startswith(prefix + "ガシャ") or message.content.startswith(prefix + "gacha") or message.content.startswith(prefix + "轉蛋") or message.content.startswith(prefix + "촬영"):
        await message.delete()
        
        try:
            if client.voice_clients[0] is not None:
                msgn = await message.channel.send(_('他のユーザーがプレイ中です。終了とクールタイムまでお待ちください。'))
                await asyncio.sleep(10)
                await msgn.delete()
                return
        except:
            pass

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
                lim = _('限定') if val[6] == 3 else ''
                pickup_alllist.append(val)
                name += count_emoji[pickup_counter] + ' ' + '［' + lim + rarity_str[val[5]] + '］' + val[1] + ' ' + val[0] + '\n'
                pickup_counter += 1

            mlgpickupemb = discord.Embed(title=_('交換カード一覧'), description=name)
            mlgpickupemb.set_author(name=author.name, icon_url=author.avatar_url)
            mlgpickupemb.set_footer(text=pickup_name)
            msgs = await message.channel.send(_('ドリームスターがカード交換数に達しているため、ガシャをご利用いただけません。カードを交換してください。\n該当番号のリアクションを返すと交換できます。'), embed=mlgpickupemb)

            for r in range(pickup_counter):
                await msgs.add_reaction(count_emoji[r])

            kind = _('ドリームスター交換') + '「' + pickup_name + '」'
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

            result = [pickup_alllist[pickup_num]]

            if result[0][5] >= 2: img = 'https://i.imgur.com/jWTTZ0d.gif'
            elif result[0][5] == 1: img = 'https://i.imgur.com/vF7fDn3.gif'
            else: img = 'https://i.imgur.com/hEHa49X.gif'

            await msgs.delete()

            print('Start MLChange[' + kind + '] by ' + str(author.id) + '.')

            if not 'SILENT' in message.content.upper() or not 'サイレント' in message.content:
                vc = await channel.connect()
                if not bgm_id == 0:
                    toBot = client.get_channel(bgm_id)
                    await toBot.send('MLGstart')

            await asyncio.sleep(0.7)
            msg = await message.channel.send(author.mention + ' https://i.imgur.com/da2w9YS.gif')
            await msg.add_reaction('👆')
            
            char_list = list()
            try:
                with open('./gacha/' + str(author.id) + '.txt', 'r') as f:
                    listline = f.read()
                    char_list = list(listline)
            except:
                pass

            with open('./gacha/' + str(author.id) + '.txt', 'w+') as f:
                try:
                    char_list[result[0][7]] = '1'
                except:
                    for n in range(500):
                        char_list.append('0')
                    char_list[result[0][7]] = '1'

                newlistline = ''.join(char_list)
                f.write(newlistline)

            await mlg_touch(msg,message,result,img,author,kind,vc,20,0)

            if vc.is_connected():
                while vc.is_playing():
                    await asyncio.sleep(2)
            return

        role = 0
        ssr_rate = 9700
        pick_rate = 99

        if pickup_name == _('ミリオンフェス'):
            ssr_rate = 9400
            pick_rate = 198

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
            print('Failed to count.')

        if len(rpicklist) == 0: rpick = rlist
        else: rpick = rpicklist

        if len(srpicklist) == 0: srpick = srlist
        else: srpick = srpicklist
        
        for n in range(role):
            if n < 9:
                rand = random.randint(0, 9999)
                if rand >= 0 and rand < 850:
                    if len(rpick) > 1:
                        result.append(rpick[random.randrange(len(rpick) - 1)])
                    else:
                        result.append(rpick[0])
                elif rand >= 850 and rand < 8500:
                    result.append(rlist[random.randrange(len(rlist) - 1)])
                elif rand >= 8500 and rand <= 8740:
                    if len(srpick) > 1:
                        result.append(srpick[random.randrange(len(srpick) - 1)])
                    else:
                        result.append(srpick[0])
                    sr_flag = 1
                elif rand >= 8740 and rand <= ssr_rate:
                    result.append(srlist[random.randrange(len(srlist) - 1)])
                    sr_flag = 1
                elif rand >= ssr_rate and rand <= ssr_rate + pick_rate:
                    if len(ssrpicklist) > 1:
                        result.append(ssrpicklist[random.randrange(len(ssrpicklist) - 1)])
                    else:
                        result.append(ssrpicklist[0])
                    ssr_flag = 1
                elif rand >= ssr_rate + pick_rate:
                    result.append(ssrlist[random.randrange(len(ssrlist) - 1)])
                    ssr_flag = 1
            elif n == 9:
                rand = random.randint(0, 9999)
                if rand >= 0 and rand <= 240:
                    if len(srpick) > 1:
                        result.append(srpick[random.randrange(len(srpick) - 1)])
                    else:
                        result.append(srpick[0])
                    sr_flag = 1
                elif rand >= 240 and rand <= ssr_rate:
                    result.append(srlist[random.randrange(len(srlist) - 1)])
                    sr_flag = 1
                elif rand >= ssr_rate and rand <= ssr_rate + pick_rate:
                    if len(ssrpicklist) > 1:
                        result.append(ssrpicklist[random.randrange(len(ssrpicklist) - 1)])
                    else:
                        result.append(ssrpicklist[0])
                    ssr_flag = 1
                elif rand >= ssr_rate + pick_rate:
                    result.append(ssrlist[random.randrange(len(ssrlist) - 1)])
                    ssr_flag = 1

        if pickup_name == _('ミリオンフェス'):
            for val in result:
                if val[5] == 3:
                    fes_flag = 1

        pink_flag = random.randint(1, 20)
        if fes_flag == 1:
            if pink_flag == 10:
                img = 'https://i.imgur.com/fGpfCgB.gif'
            elif pink_flag == 20:
                img = 'https://i.imgur.com/jWTTZ0d.gif'
            else:
                img = 'https://i.imgur.com/0DxyVhm.gif'
        elif ssr_flag == 1 and not fes_flag == 1:
            img = 'https://i.imgur.com/jWTTZ0d.gif'
        elif sr_flag == 1 and not fes_flag == 1 and not ssr_flag == 1:
            img = 'https://i.imgur.com/vF7fDn3.gif'
        else:
            img = 'https://i.imgur.com/hEHa49X.gif'

        print('Start MLGacha[' + pickup_name + '] by ' + author.name + '.')

        char_list = list()
        try:
            with open('./gacha/' + str(author.id) + '.txt', 'r') as f:
                listline = f.read()
                char_list = list(listline)
        except:
            pass

        for box in result:
            with open('./gacha/' + str(author.id) + '.txt', 'w+') as f:
                try:
                    char_list[box[7]] = '1'
                except:
                    for n in range(500):
                        char_list.append('0')
                    char_list[box[7]] = '1'

                newlistline = ''.join(char_list)
                f.write(newlistline)

        mess = random.randint(1,10)
        phrase = str()
        if mess >= 2 and (ssr_flag == 1 or fes_flag == 1): phrase = _('最高の一枚ができましたのでぜひご確認ください！')
        elif mess <= 4 and (sr_flag == 1 or ssr_flag == 1 or fes_flag == 1): phrase = _('みんなのいい表情が撮れました！')
        elif mess > 4 and mess <= 8 and (sr_flag == 1 or ssr_flag == 1 or fes_flag == 1): phrase = _('楽しそうなところが撮れましたよ')

        if not 'SILENT' in message.content.upper() or not 'サイレント' in message.content:
            vc = await channel.connect()

            if not len(phrase) == 0:
                vc.play(discord.FFmpegPCMAudio('./resources/message.mp3'))
                camera = await message.channel.send(phrase)
                while vc.is_playing():
                    await asyncio.sleep(3)
                await camera.delete()

            if not bgm_id == 0:
                toBot = client.get_channel(bgm_id)
                await toBot.send('MLGstart')

        waitemb = discord.Embed()

        await asyncio.sleep(0.7)
        if fes_flag == 1 and pink_flag == 10: waitemb.set_image(url='https://i.imgur.com/ZC8JK9i.gif')
        else: waitemb.set_image(url='https://i.imgur.com/da2w9YS.gif')
            
        waitemb.set_footer(text=pickup_name)
        waitemb.set_image(url='https://i.imgur.com/da2w9YS.gif')
        msg = await message.channel.send(message.author.mention, embed=waitemb)
        await msg.add_reaction('👆')

        await mlg_touch(msg,message,result,img,author,pickup_name,vc,pink_flag,fes_flag)
            
        if vc.is_connected():
            while vc.is_playing():
                await asyncio.sleep(2)

async def gacha_reload(flag,message):
    global mlg_all, feslist, ssrlist, srlist, rlist, ssrpicklist, srpicklist, rpicklist, pickup, pickup_name
    print('----------[MLG v2.0.0 MLreload]----------')
    if flag == 1: msg = await message.channel.send('MLreload Start.')

    ssrlist = []
    srlist = []
    rlist = []
    feslist = []
    mlg_all = []
    pickup = []
    ssrpicklist = []
    srpicklist = []
    rpicklist = []
    print('MLG temporary data cleaned.')
    if flag == 1: await msg.edit(content='MLG temporary data cleaned.')

    if lang == 'ja':
        url1 = 'https://dl.dropboxusercontent.com/s/tzefjf3bkzft6kk/mlg_all.csv'
        url2 = 'https://dl.dropboxusercontent.com/s/xktk86nhgcvu7ax/pickup_name.txt'
    elif lang == 'cn':
        url1 = 'https://dl.dropboxusercontent.com/s/mirwbbfujj9y7t8/mlg_all_cn.csv'
        url2 = 'https://dl.dropboxusercontent.com/s/34v5er4l4drczxy/pickup_name_cn.txt'
    elif lang == 'kr':
        url1 = 'https://dl.dropboxusercontent.com/s/qgo5tjm3qbb3tdo/mlg_all_kr.csv'
        url2 = 'https://dl.dropboxusercontent.com/s/ae5zzjb2wgsodkt/pickup_name_kr.txt'
    else:
        url1 = 'https://dl.dropboxusercontent.com/s/tzefjf3bkzft6kk/mlg_all.csv'
        url2 = 'https://dl.dropboxusercontent.com/s/xktk86nhgcvu7ax/pickup_name.txt'

    request.urlretrieve(url1,'./gacha_data/mlg_all.csv')
    print('MLG data "mlg_all.csv" Downloaded.')
    if flag == 1: await msg.edit(content='MLG data "mlg_all.csv" Downloaded.')
    request.urlretrieve(url2,'./gacha_data/pickup_name.txt')
    print('MLG data "pickup_name.txt" Downloaded.')
    if flag == 1: await msg.edit(content='MLG data "mlg_all.csv" Downloaded.')
    
    with open('./gacha_data/pickup_name.txt',encoding="utf-8_sig") as f:
        pickup_name = f.read()

    fescount = 0
    ssrcount = 0
    srcount = 0
    rcount = 0
    with open('./gacha_data/mlg_all.csv',encoding="utf-8_sig") as f:
        reader = csv.reader(f)
        for row in reader:
            indata = [row[3],str(row[4]),row[5],row[6],str(row[7]),int(row[2]),int(row[1]),int(row[0])]
            mlg_all.insert(0, indata)
            fesmode = 'FES mode unavailable.'

            if indata[5] == 3:
                fescount += 1
                if indata[6] >= 2:
                    fesmode = 'FES mode AVAILABLE.'
                    ssrpicklist.append(indata)
                    pickup.append(indata)
                else:
                    feslist.insert(0, indata)
            elif indata[5] == 2 and not int(row[1]) == 0:
                ssrcount += 1
                if indata[6] >= 2:
                    ssrpicklist.append(indata)
                    pickup.append(indata)
                else:
                    ssrlist.insert(0, indata)
            elif indata[5] == 1 and not int(row[1]) == 0:
                srcount += 1
                if indata[6] >= 2:
                    srpicklist.append(indata)
                    pickup.append(indata)
                else:
                    srlist.insert(0, indata)
            elif indata[5] == 0:
                rcount += 1
                if indata[6] >= 2:
                    rpicklist.append(indata)
                    pickup.append(indata)
                else:
                    rlist.insert(0, indata)

    print('Loaded ' + str(len(mlg_all)) + ' cards.')
    print('Users can get ' + str(fescount + ssrcount + srcount + rcount) + ' kinds of cards. ([FES]' + str(fescount) + ', [SSR]' + str(ssrcount) + ', [SR]' + str(srcount) + ', [R]' + str(rcount) + ')')
    print('Pickup name is 「' + pickup_name + '」 ' + fesmode)
    print('Pickup cards')
    name = ''
    for row in pickup:
        lim = 'Limited ' if row[6] == 3 else ''
        print('[' + lim + rarity_str[row[5]] + ']' + row[1] + ' ' + row[0])
        name += '[' + lim + rarity_str[row[5]] + ']' + row[1] + ' ' + row[0] + '\n'

    emb = discord.Embed(title='Pickup Cards', description=name)
    emb.set_author(name=pickup_name)

    if flag == 1: await msg.edit(content='Loaded ' + str(len(mlg_all)) + ' cards.\n' +\
        'Users can get ' + str(fescount + ssrcount + srcount + rcount) + ' kinds of cards. ([FES]' + str(fescount) + ', [SSR]' + str(ssrcount) + ', [SR]' + str(srcount) + ', [R]' + str(rcount) + ')\n' +\
        'Pickup name is 「' + pickup_name + '」 ' + fesmode + '\n' +\
        'All MLreload process completed successfully.', embed=emb)
    print('All MLreload process completed successfully.')
    print('-----------------------------------------')

    await reload_timer(60)
    return

async def reload_timer(time):
    global timer
    timer = time
    while timer > 0:
        timer -= 1
        await asyncio.sleep(2)
    return timer

async def gacha_note(message):
    char_list = list()
    try:
        with open('./gacha/' + str(message.author.id) + '.txt', 'r') as f:
            listline = f.read()
            char_list = list(listline)
    except:
        import traceback
        traceback.print_exc()
        await message.channel.send(message.author.mention + _('所持SSRの記録がないか、エラーが発生しました。'))
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

        text[page] += '\n[' + rarity_str[val[5]] + ']' + val[1] + ' ' + val[0]

    gacha_count = str()
    try:
        with open('./gacha_count/' + str(message.author.id) + '.txt', 'r') as f:
            gacha_count = f.read()
    except:
        gacha_count = '0'

    fotter_text = _('ドリームスター所持数：') + gacha_count

    now = 1

    emb = discord.Embed(title=_('所持SSR一覧') + ' Page ' + str(now) + '/' + str(len(text)), description=text[now - 1])
    emb.set_author(name=message.author.name, icon_url=message.author.avatar_url)
    emb.set_footer(text=fotter_text)
    msg = await message.channel.send(_('見終わったら×で消してね！'), embed=emb)
    await msg.add_reaction('◀')
    await msg.add_reaction('▶')
    await msg.add_reaction('❌')

    while True:
        try:
            target_reaction, user = await client.wait_for('reaction_add', timeout=timeout)

            if target_reaction.emoji == '◀' and user != msg.author:
                if not now == 1:
                    now -= 1
                    emb = discord.Embed(title=_('所持SSR一覧') + ' Page ' + str(now) + '/' + str(len(text)), description=text[now - 1])
                    emb.set_author(name=message.author.name, icon_url=message.author.avatar_url)
                    emb.set_footer(text=fotter_text)
                    await msg.edit(embed=emb)
                else:
                    now = len(text)
                    emb = discord.Embed(title=_('所持SSR一覧') + ' Page ' + str(now) + '/' + str(len(text)), description=text[now - 1])
                    emb.set_author(name=message.author.name, icon_url=message.author.avatar_url)
                    emb.set_footer(text=fotter_text)
                    await msg.edit(embed=emb)
                await msg.remove_reaction(target_reaction.emoji, user)
            elif target_reaction.emoji == '▶' and user != msg.author:
                if not now == len(text):
                    now += 1
                    emb = discord.Embed(title=_('所持SSR一覧') + ' Page ' + str(now) + '/' + str(len(text)), description=text[now - 1])
                    emb.set_author(name=message.author.name, icon_url=message.author.avatar_url)
                    emb.set_footer(text=fotter_text)
                    await msg.edit(embed=emb)
                else:
                    now = 1
                    emb = discord.Embed(title=_('所持SSR一覧') + ' Page ' + str(now) + '/' + str(len(text)), description=text[now - 1])
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
            await msg.edit(content=_('しばらく操作がなかったため、タイムアウトしました。'),embed=None)
            await asyncio.sleep(10)
            await msg.delete()
            break

async def mlg_touch(msg,message,result,img,author,kind,vc,pink_flag,fes_flag):
    try:
        log = ''
        count = 0
        ssr_skip = []
        ssr_count = []
        while True:
            target_reaction, user = await client.wait_for('reaction_add', timeout=timeout)
            if user == author and target_reaction.emoji == '👆':
                await msg.clear_reactions()
                openemb = discord.Embed()
                openemb.set_footer(text=pickup_name)
                openemb.set_image(url=img)
                await msg.edit(embed=openemb)

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
                player_show = discord.FFmpegPCMAudio('./resources/fes.mp3')
                await msg.clear_reactions()
            elif result_10[5] == 2:
                player_show = discord.FFmpegPCMAudio('./resources/ssr.mp3')
                await msg.clear_reactions()
            elif result_10[5] <= 1:
                player_show = discord.FFmpegPCMAudio('./resources/normal.mp3')

            desc = rarity_str[result_10[5]] + '　' + result_10[1] + '　' + result_10[0]
            if lang == 'ja': lang_data = 0
            elif lang == 'cn': lang_data = 4
            elif lang == 'kr': lang_data = 6
            else: lang_data = 0
            for data in imas.million_data:
                if result_10[0] in data[lang_data]:
                    color = data[3]
                    cv = 'CV.' + data[lang_data + 1]
            mlgnormalemb = discord.Embed(title=desc, description=cv, colour=color)

            footer_text = kind + ' ' + str((count + 1)) + '/' + str(len(result))
            mlgnormalemb.set_author(name=author.name, icon_url=author.avatar_url)
            mlgnormalemb.set_footer(text=footer_text)

            mlgnormalemb.set_image(url=result_10[2])
            if vc.is_connected(): vc.play(player_show)

            #カード表示（SSRの場合特訓前）
            await msg.edit(content=author.mention, embed=mlgnormalemb)

            if result_10[5] >= 2:
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
                    if vc.is_connected() and vc.is_playing(): vc.stop()
                    count += 1
                    log += '[' + rarity_str[result_10[5]] + ']' + result_10[1] + ' ' + result_10[0] + '\n'
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
                        mlglogemb = discord.Embed(title=_('ガシャ結果'), description=log + '\n' + _('ドリームスター所持数：') + gacha_count)
                        mlglogemb.set_author(name=author.name, icon_url=author.avatar_url)
                        mlglogemb.set_footer(text=footer_text)
                        await toLog.send(embed=mlglogemb)

                        return
                    else:
                        await msg.remove_reaction(target_reaction2.emoji, user)
                    break
                elif target_reaction2.emoji == '⏭' and user == author:
                    for n,box in enumerate(result):
                        if count > n:
                            continue
                        log += '[' + rarity_str[box[5]] + ']' + box[1] + ' ' + box[0] + '\n'
                        if box[5] >= 2:
                            ssr_skip.append(box)
                            ssr_count.append(n+1)

                    if len(ssr_skip) > 0:
                        for n,result_ssr in enumerate(ssr_skip):
                            if result_ssr[5] == 3:
                                player_show = discord.FFmpegPCMAudio('./resources/fes.mp3')
                                await msg.clear_reactions()
                            elif result_ssr[5] == 2:
                                player_show = discord.FFmpegPCMAudio('./resources/ssr.mp3')
                                await msg.clear_reactions()

                            desc = rarity_str[result_ssr[5]] + '　' + result_ssr[1] + '　' + result_ssr[0]
                            if lang == 'ja': lang_data = 0
                            elif lang == 'cn': lang_data = 4
                            elif lang == 'kr': lang_data = 6
                            else: lang_data = 0
                            for data in imas.million_data:
                                if result_ssr[0] in data[lang_data]:
                                    color = data[3]
                                    cv = 'CV.' + data[lang_data + 1]
                            mlgnormalemb = discord.Embed(title=desc, description=cv, colour=color)

                            footer_text = kind + ' ' + ssr_count[n+1] + '/' + str(len(result))
                            mlgnormalemb.set_author(name=author.name, icon_url=author.avatar_url)
                            mlgnormalemb.set_footer(text=footer_text)

                            mlgnormalemb.set_image(url=result_ssr[2])
                            if vc.is_connected() and vc.is_playing():
                                vc.stop()
                                vc.play(player_show)

                            await msg.edit(content=author.mention, embed=mlgnormalemb)

                            if vc.is_connected():
                                while vc.is_playing():
                                    await asyncio.sleep(1)
                                vc.play(discord.FFmpegPCMAudio('./resources/ssr_talk.mp3'))

                            line = result_ssr[4].replace('ProP', author.name + 'P')
                            mlgssremb = discord.Embed(title=desc, description=cv, colour=color)
                            mlgssremb.set_footer(text=footer_text, icon_url=author.avatar_url)
                            mlgssremb.set_image(url=result_ssr[3])

                            await asyncio.sleep(4.2)
                            await msg.edit(content=author.mention, embed=mlgssremb)
                            await asyncio.sleep(3)
                            await msg.edit(content=result_ssr[0] + '「' + line + '」', embed=mlgssremb)

                            await msg.add_reaction('👆')
                            while True:
                                target_reaction2, user = await client.wait_for('reaction_add')

                                if target_reaction2.emoji == '👆' and user == author:
                                    if vc.is_connected() and vc.is_playing(): vc.stop()
                                    count += 1
                                    await msg.remove_reaction(target_reaction2.emoji, user)
                                    break

                    if vc.is_connected():
                        if not bgm_id == 0:
                            toBot = client.get_channel(bgm_id)
                            await toBot.send('disconnect')
                        await vc.disconnect()

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
                    mlglogemb = discord.Embed(title=_('ガシャ結果'), description=log + '\n' + _('ドリームスター所持数：') + gacha_count)
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
        await message.channel.send(_('しばらく操作がなかったため、タイムアウトしました。'))
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