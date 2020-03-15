#coding: utf-8
#created by @hiromin0627
#MilliShita Gacha v5
mlgbotver = '5.0.0_beta'

import glob
import gettext
import os
import discord
import asyncio
import re,random
import datetime
from threading import (Event, Thread)
from urllib import request
import configparser
import json

ini = configparser.ConfigParser()
ini.read('./config.ini', 'UTF-8')

lang = ini['Language']['lang']

path_to_locale_dir = os.path.abspath(os.path.join(os.path.dirname(__file__),'./locale'))
if lang == 'cn': translang = 'zh_TW'
elif lang == 'kr': translang = 'ko_KR'
else: translang = 'ja_JP'
translater = gettext.translation('messages',localedir=path_to_locale_dir,languages=[translang],fallback=True,codeset="utf8")
translater.install()

token = ini['tokens']['token']

bgm_id = int(ini['ids']['bgm-room'])
log_id = int(ini['ids']['log-room'])

version = ini['Data']['Version']

prefix = ini['Prefix']['commandprefix']

timeout = float(ini['Reaction']['timeout'])
aftermsgdel = ini['Reaction']['aftermsgdel']

client = discord.Client()

mlg_all = [[],[],[]]
mlg_data = [[],[],[]]
pickup_id = [[],[],[]]

pickup_name = ['','','']
pickup_img = ['','','']
rarity_str = ['R','SR','SSR','FES']
langnamelist = ['ja','kr','cn']

timer = 0

@client.event
async def on_ready():
    print(strtimestamp() + '---Millishita Gacha ' + mlgbotver + '---')
    print(strtimestamp() + 'discord.py ver:' + discord.__version__)
    print(strtimestamp() + 'Logged in as ' + client.user.name + '(ID:' + str(client.user.id) + ')')
    print(strtimestamp() + 'Bot created by @hiromin0627')
    await gacha_reload(0,None)

@client.event
async def on_message(message):
    if message.author.bot:
        return

    if message.content.startswith("MLhelp"):
        if not aftermsgdel == 'false': await message.delete()
        print(strtimestamp() + 'Start MLhelp')
        await message.channel.send('ミリシタガシャシミュレーターDiscordボット ' + mlgbotver + '\n' +\
            'MLhelp：ヘルプコマンドです。ミリシタガシャの説明を見ることができます。\n' +\
            prefix + 'update：ミリシタガシャデータベースをダウンロードして更新します。\n' +\
            prefix + 'reload：ミリシタガシャデータベースをローカルファイルを用いて更新します。\n' +\
            prefix + 'reset：全ユーザーのMLガシャを引いた回数をリセットします。\n' +\
            prefix + 'cards：MLガシャで引いたカード名を確認することができます。\n' +\
            prefix + 'pickup：現在のガシャ名とピックアップカードを確認できます。\n' +\
            prefix + 'call：MLガシャで引いたカード画像を検索できます。スペースを挟んでカード名を入力してください。（制服シリーズはアイドル名も記入）\n' +\
            prefix + 'ガシャ or ' + prefix + '轉蛋 or ' + prefix + '촬영 or ' + prefix + 'gacha：ミリシタガシャシミュレーターができます。' +\
            '10を後ろに付け加えると、10連ガシャになります。jp（日本語版）、cn（中国語繁体字版）、kr（韓国語版）を後ろに付け加えると、その言語のガシャが引くことができます。')
        
    if message.content.startswith(prefix):
        if not aftermsgdel == 'false':
            if "reload" in message.content or "update" in message.content or "update" in message.content or "cards" in message.content or "reset" in message.content or "pickup" in message.content or "call" in message.content or "ガシャ" in message.content or "gacha" in message.content or "轉蛋" in message.content or "촬영" in message.content:
                await message.delete()

        langint = 0
        if not message.content == '':
            langint = langstrtoint(message.content[6:])
        else:
            langint = langtoint()

        if message.content.startswith(prefix + "reload"):
            await gacha_reload(1,message)
        elif message.content.startswith(prefix + "update"):
            global version
            latest = gacha_check_update()

            current = dict()
            try:
                with open('./gacha_data/version.json', 'r') as f:
                    current = json.load(f)
            except:
                with open('./gacha_data/version.json', 'w') as f:
                    pre = {"date": "Data unavailable. Please update mlg data.","dlurl": ""}
                    json.dump(pre, f)
                    current = pre

            if latest["date"] == current["date"]:
                msgl = await message.channel.send('現在のガシャデータベースは最新のものが使われています。')
                return
            elif not version == "Latest":
                msgl = await message.channel.send('バージョンが設定ファイルで指定されています。最新のガシャデータベース：' + latest["date"] + '\n現在のガシャデータベース：' + current["date"] + '\n設定を「Latest」に上書きしてアップデートしますか？')
                await msgl.add_reaction('⭕')
                await msgl.add_reaction('❌')
                flag = 1
            else:
                msgl = await message.channel.send('最新のガシャデータベース：' + latest["date"] + '\n現在のガシャデータベース：' + current["date"] + '\nアップデートしますか？')
                await msgl.add_reaction('⭕')
                await msgl.add_reaction('❌')
                flag = 0

                while True:
                    try:
                        target_reaction, user = await client.wait_for('reaction_add', timeout=timeout)

                        if target_reaction.emoji == '⭕' and user != msgl.author:
                            await msgl.edit(content='アップデートを開始します。')
                            await msgl.clear_reactions()
                            version = latest["date"]
                            if flag == 1:
                                ini.set("Data", "Version", "Latest")
                                ini.write(open('./config.ini', 'w'), 'UTF-8')
                            with open('./gacha_data/version.json', 'w') as f:
                                json.dump(latest, f)
                            await gacha_reload(1, message)
                            await msgl.edit(content='アップデートが完了しました。')
                            return
                        if target_reaction.emoji == '❌' and user != msgl.author:
                            await msgl.edit(content='アップデートを中止します。')
                            return
                    except:
                        await msgl.edit(content='コマンドに失敗しました。もう一度やり直してください。')
                        return
        elif message.content.startswith(prefix + 'cards'):
            print(strtimestamp() + 'Start MLGacha[cards].')
            await gacha_note(message,langint)
        elif message.content.startswith(prefix + 'reset'):
            print(strtimestamp() + 'Start MLGacha[reset].')
            file_list = glob.glob("./gacha_count/*.txt")
            for file in file_list:
                os.remove(file)
            await message.channel.send(_('すべてのユーザーのガチャカウントをリセットしました。'))
        elif message.content.startswith(prefix + 'pickup'):
            print(strtimestamp() + 'Start MLGacha[pickup].')

            name = pickupcheck(langint)

            emb = discord.Embed(title=_('ピックアップカード一覧'), description=name)
            emb.set_image(url=pickup_img[langint])
            emb.set_author(name=pickup_name[langint])
            await message.channel.send('', embed=emb)
        elif message.content.startswith(prefix + 'call'):
            print(strtimestamp() + 'Start MLGacha[call].')
            await gacha_call(message,langint)
        elif message.content.startswith(prefix + "ガシャ") or message.content.startswith(prefix + "gacha") or message.content.startswith(prefix + "轉蛋") or message.content.startswith(prefix + "촬영"):
            if voicecheck():
                await message.channel.send(_('他のユーザーがプレイ中です。終了までお待ちください。'))
                return

            gacha_count = int()

            try:
                with open('./gacha_count/' + langnamelist[langint] + str(message.author.id) + '.txt', 'r') as f:
                    gacha_count = int(f.read())
            except:
                with open('./gacha_count/' + langnamelist[langint] + str(message.author.id) + '.txt', 'w') as f:
                    f.write('0')

            if gacha_count >= 300:
                await gacha_prepare_select(message,langint)
            else:
                await gacha_prepare(message,langint,gacha_count)

async def gacha_prepare_select(message,langint):
    try:
        vc_id = message.author.voice.channel.id
        channel = client.get_channel(vc_id)
    except:
        vc_id = None

    kind = ''
    result = []

    count_emoji = ['1⃣','2⃣','3⃣','4⃣','5⃣','6⃣','7⃣','8⃣','9⃣','🔟']
    pickup_counter = 0
    pickup_alllist = list()

    name = pickupcheck(langint)
    global version
    url = "https://data.hiromin.xyz/gachadata"
    readObj = request.urlopen(url)
    response = readObj.read()
    data = json.loads(response)
    pickup_id = data[version]["pickupIDs"]
    for row in mlg_data[langint]:
        if row["id"] in pickup_id:
            pickup_alllist.append(row)
            pickup_counter += 1

    mlgpickupemb = discord.Embed(title=_('交換カード一覧'), description=name)
    mlgpickupemb.set_author(name=message.author.name, icon_url=message.author.avatar_url)
    mlgpickupemb.set_footer(text=pickup_name[langint])
    msgs = await message.channel.send(_('ドリームスターがカード交換数に達しているため、ガシャをご利用いただけません。カードを交換してください。\n該当番号のリアクションを返すと交換できます。'), embed=mlgpickupemb)

    for r in range(pickup_counter):
        await msgs.add_reaction(count_emoji[r])

    kind = _('ドリームスター交換') + '「' + pickup_name[langint] + '」'

    pickup_num = int()
    numemoji_to_int = {'1⃣':0, '2⃣':1, '3⃣':2, '4⃣':3, '5⃣':4, '6⃣':5, '7⃣':6, '8⃣':7, '9⃣':8, '🔟':9}
    while True:
        target_reaction, user = await client.wait_for('reaction_add')
        if not user == msgs.author:
            if target_reaction.emoji in numemoji_to_int:
                pickup_num = numemoji_to_int[target_reaction.emoji]
                break

    result = [pickup_alllist[pickup_num]]

    await msgs.delete()

    print(strtimestamp() + 'Start MLChange[' + kind + '] by ' + str(message.author.id) + '.')
    
    try:
        with open('./gacha_count/' + langnamelist[langint] + str(message.author.id) + '.txt', 'w') as f:
            f.write(str(0))
    except:
        print(strtimestamp() + '[ERROR]Gacha count FAILED.')

    char_list = list()
    try:
        with open('./gacha/' + langnamelist[langint] + str(message.author.id) + '.txt', 'r') as f:
            listline = f.read()
            char_list = list(listline)
    except:
        pass

    with open('./gacha/' + langnamelist[langint] + str(message.author.id) + '.txt', 'w+') as f:
        try:
            char_list[result[0]["id"]] = '1'
        except:
            for n in range(500):
                char_list.append('0')
            char_list[result[0]["id"]] = '1'

        newlistline = ''.join(char_list)
        f.write(newlistline)

    if vc_id == None:
        vc = None
        botmsg = None
    else:
        if not bgm_id == 0:
            toBot = client.get_channel(bgm_id)
            botmsg = await toBot.send('ML' + str(vc_id))
        vc = await channel.connect()

    await mlg_touch(message,result,kind,vc,botmsg,langint)
    return

async def gacha_prepare(message,langint,gacha_count):
    try:
        vc_id = message.author.voice.channel.id
        channel = client.get_channel(vc_id)
    except:
        vc_id = None

    result = []
    role = 0
    ssr_rate = 9700
    pick_rate = 99

    if pickup_name[langint] == 'ミリオンフェス' or pickup_name[langint] == '百萬祭典' or pickup_name[langint] == '밀리언 페스티벌':
        ssr_rate = 9400
        pick_rate = 198

    if '10' in message.content or '１０' in message.content:
        role = 10
    else:
        role = 1

    try:
        gacha_count += role
        with open('./gacha_count/' + langnamelist[langint] + str(message.author.id) + '.txt', 'w') as f:
            f.write(str(gacha_count))
    except:
        print(strtimestamp() + '[ERROR]Failed to count.')

    rpick = list()
    rcard = list()
    srpick = list()
    srcard = list()
    ssrpick = list()
    ssrcard = list()

    for row in mlg_data[langint]:
        if row["rarity"] == 0 and row["id"] in pickup_id[langint]:
            rpick.append(row)
        elif row["rarity"] == 0 and not row["id"] in pickup_id[langint]:
            rcard.append(row)
        elif row["rarity"] == 1 and row["id"] in pickup_id[langint]:
            srpick.append(row)
        elif row["rarity"] == 1 and not row["id"] in pickup_id[langint]:
            srcard.append(row)
        elif row["rarity"] >= 2 and row["id"] in pickup_id[langint]:
            ssrpick.append(row)
        elif row["rarity"] >= 2 and not row["id"] in pickup_id[langint]:
            ssrcard.append(row)

    if len(rpick) == 0: rpick = rcard
    if len(srpick) == 0: srpick = srcard
    
    for n in range(role):
        if n < 9:
            rand = random.randint(0, 9999)
            if rand >= 0 and rand < 850:
                if len(rpick) > 1:
                    result.append(rpick[random.randrange(len(rpick) - 1)])
                else:
                    result.append(rpick[0])
            elif rand >= 850 and rand < 8500:
                result.append(rpick[random.randrange(len(rpick) - 1)])
            elif rand >= 8500 and rand <= 8740:
                if len(srpick) > 1:
                    result.append(srpick[random.randrange(len(srpick) - 1)])
                else:
                    result.append(srpick[0])
            elif rand >= 8740 and rand < ssr_rate:
                result.append(srcard[random.randrange(len(srcard) - 1)])
            elif rand >= ssr_rate and rand <= ssr_rate + pick_rate:
                if len(ssrpick) > 1:
                    result.append(ssrpick[random.randrange(len(ssrpick) - 1)])
                else:
                    result.append(ssrpick[0])
            elif rand >= ssr_rate + pick_rate:
                result.append(ssrcard[random.randrange(len(ssrcard) - 1)])
        elif n == 9:
            rand = random.randint(0, 9999)
            if rand >= 0 and rand <= 240:
                if len(srpick) > 1:
                    result.append(srpick[random.randrange(len(srpick) - 1)])
                else:
                    result.append(srpick[0])
            elif rand >= 240 and rand <= ssr_rate:
                result.append(srcard[random.randrange(len(srcard) - 1)])
            elif rand >= ssr_rate and rand <= ssr_rate + pick_rate:
                if len(mlg_data[langint][5]) > 1:
                    result.append(ssrpick[random.randrange(len(ssrpick) - 1)])
                else:
                    result.append(ssrpick[0])
            elif rand >= ssr_rate + pick_rate:
                result.append(ssrcard[random.randrange(len(ssrcard) - 1)])

    print(strtimestamp() + 'Start MLGacha[' + pickup_name[langint] + '] by ' + message.author.name + '.')

    char_list = list()
    try:
        with open('./gacha/' + langnamelist[langint] + str(message.author.id) + '.txt', 'r') as f:
            listline = f.read()
            char_list = list(listline)
    except:
        pass

    for box in result:
        with open('./gacha/' + langnamelist[langint] + str(message.author.id) + '.txt', 'w+') as f:
            try:
                char_list[box["id"]] = '1'
            except:
                for n in range(500):
                    char_list.append('0')
                char_list[box["id"]] = '1'

            newlistline = ''.join(char_list)
            f.write(newlistline)

    mess = random.randint(1,10)
    fes_flag = 0
    ssr_flag = 0
    sr_flag = 0
    for val in result:
        if val["rarity"] == 3:
            fes_flag = 1
        elif val["rarity"] == 2:
            ssr_flag = 1
        elif val["rarity"] == 1:
            sr_flag = 1
    phrase = [_('最高の一枚ができましたのでぜひご確認ください！'),_('みんなのいい表情が撮れました！'),_('楽しそうなところが撮れましたよ')]
    cameratxt = ''
    if mess >= 2 :
        if ssr_flag == 1 or fes_flag == 1: cameratxt = phrase[0]
        elif sr_flag == 1 or ssr_flag == 1 or fes_flag == 1: cameratxt = phrase[1]
        elif sr_flag == 1 or ssr_flag == 1 or fes_flag == 1: cameratxt = phrase[2]

    if vc_id == None:
        vc = None
        botmsg = None
        if not cameratxt == '':
            camera = await message.channel.send(cameratxt)
            await asyncio.sleep(3)
            await camera.delete()
    else:
        vc = await channel.connect()
        if not cameratxt == '':
            vc.play(discord.FFmpegPCMAudio('./resources/message.mp3'))
            camera = await message.channel.send(cameratxt)
            while vc.is_playing():
                await asyncio.sleep(1)
            await camera.delete()
        if not bgm_id == 0:
            toBot = client.get_channel(bgm_id)
            botmsg = await toBot.send('ML' + str(vc_id))

    await mlg_touch(message,result,pickup_name[langint],vc,botmsg,langint)

async def gacha_call(message,langint):
    char_list = list()
    carddata = {}

    try:
        with open('./gacha/' + langnamelist[langint] + str(message.author.id) + '.txt', 'r') as f:
            listline = f.read()
            char_list = list(listline)
    except:
        print(strtimestamp() + '[ERROR]Failed to load gacha result file.')
        return

    if '制服シリーズ' in message.content[6:]:
        for data in mlg_all[langint]:
            if message.content[6:] in data["idol"] and data["name"] == '制服シリーズ':
                carddata = data
                break
    elif 'シアターデイズ' in message.content[6:] or '劇場時光' in message.content[6:] or '시어터 데이즈' in message.content[6:]:
        for data in mlg_all[langint]:
            if data["idol"] in message.content[6:] and (data["name"] == 'シアターデイズ' or data["name"] == '劇場時光' or data["name"] == '시어터 데이즈'):
                carddata = data
                break
    else:
        for data in mlg_all[langint]:
            if data["name"] in message.content[6:] and char_list[data["id"]] == '1':
                carddata = data
                break

    if len(carddata) == 0:
        msgn = await message.channel.send(_('カードが見つかりませんでした。\n「MLcheck」で自分が所持しているカード名を確認してください。'))
        await asyncio.sleep(10)
        await msgn.delete()
        return

    cardname = '[' + rarity_str[int(carddata["rarity"])] + ']' + carddata["name"] + ' ' + carddata["idol"]
    embmsg1 = discord.Embed(title=cardname, description='(CV.' + carddata["cv"] + ')', colour=int(carddata["color"], 0))
    embmsg1.set_author(name=message.author.name + _('所持カード'), icon_url=message.author.avatar_url)
    embmsg1.set_image(url=carddata["image"])
    msg = await message.channel.send('', embed=embmsg1)
    await msg.add_reaction('👆')
    while True:
        target_reaction, user = await client.wait_for('reaction_add')
        if target_reaction.emoji == '👆' and user != msg.author:
            if carddata["rarity"] >= 2:
                await msg.remove_reaction(target_reaction.emoji, user)
                cardname = '[' + rarity_str[int(carddata["rarity"])] + '+]' + carddata["name"] + ' ' + carddata["idol"]
                embmsg1 = discord.Embed(title=cardname, description='(CV.' + carddata["cv"] + ')', colour=int(carddata["color"], 0))
                embmsg1.set_author(name=message.author.name + _('所持カード'), icon_url=message.author.avatar_url)
                embmsg1.set_image(url=carddata["imageAwake"])
                await msg.edit(embed=embmsg1)
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

def gacha_check_update():
    url = "https://data.hiromin.xyz/latest"
    readObj = request.urlopen(url)
    response = readObj.read()
    data = json.loads(response)
    return data

async def gacha_reload(flag,message):
    global mlg_all, mlg_data, pickup_id, version
    print(strtimestamp() + '----------[MLG ' + mlgbotver + ' MLreload]----------')
    if flag == 1: msg = await message.channel.send('MLreload Start.')
    
    mlg_all = [[],[],[]]
    mlg_data = [[],[],[]]
    pickup_id = [[],[],[]]
    name = ['','','']
    print(strtimestamp() + 'MLG temporary data cleaned.')
    if flag == 1: await msg.edit(content='MLG temporary data cleaned.')

    url = "https://data.hiromin.xyz/"

    if version == "Latest":
        readObj_latest = request.urlopen(url+"latest")
        response = readObj_latest.read()
        data = json.loads(response)
        mlgver = str(data["date"])
        with open('./gacha_data/version.json', 'w') as f:
            json.dump(data, f)
    else:
        data = {"date": version}
        mlgver = version
        with open('./gacha_data/version.json', 'w') as f:
            json.dump(data, f)

    print(strtimestamp() + 'Using version "' + mlgver + '". Start to load card datas.')
    
    readObj_gachadata = request.urlopen(url+"gachadata")
    response_gachadata = readObj_gachadata.read()
    info = json.loads(response_gachadata)

    for langint,langname in enumerate(langnamelist):
        pickup_id[langint] = info[mlgver]["pickupIDs"][langname]
    
    readObj_cards = request.urlopen(url+"cards")
    response_cards = readObj_cards.read()
    reader = json.loads(response_cards)

    for langint,langname in enumerate(langnamelist):
        count = [0,0,0,0]
        print('[Step ' + str(langint + 1) + '/3 (Lang:' + langname + ')]')
        if flag == 1: await msg.edit(content='MLG Database Loading... \nStep ' + str(langint + 1) + '/3 (Lang:' + langname + ')')

        pickup_img[langint] = info[mlgver]["gachaImageUrl"][langname]
        pickup_name[langint] = info[mlgver]["gachaName"][langname]
        
        mlg_all[langint] = reader[langname]
        if not len(info[mlgver]["activeIDs"][langname]) == 0:
            pickup_id[langint] = info[mlgver]["activeIDs"][langname]
            for row in reader[langname]:
                if row["id"] in info[mlgver]["activeIDs"][langname]:
                    mlg_data[langint].append(row)
                    count[row["rarity"]] += 1
        else:
            pickup_id[langint] = info[mlgver]["pickupIDs"][langname]
            for row in reader[langname]:
                if not row["limited"]:
                    mlg_data[langint].append(row)
                    count[row["rarity"]] += 1
                elif row["limited"] and row["id"] in pickup_id[langint]:
                    mlg_data[langint].append(row)
                    count[row["rarity"]] += 1
                elif row["rarity"] == 3 and info[mlgver]["fes"][langname]:
                    mlg_data[langint].append(row)
                    count[row["rarity"]] += 1

        print('Pickup name is 「' + pickup_name[langint] + '」')
        print('Pickup cards')
        for row in mlg_data[langint]:
            if row["id"] in pickup_id[langint]:
                lim = _('限定') if row["limited"] == True else ''
                print('[' + lim + rarity_str[row["rarity"]] + ']' + row["name"] + ' ' + row["idol"] + ' (CV.' + row["cv"] + ')')
                name[langint] += '［' + lim + rarity_str[row["rarity"]] + '］' + row["name"] + ' ' + row["idol"] + ' (CV.' + row["cv"] + ')\n'
        print('Actived ' + str(len(mlg_data[langint])) + ' cards.([FES]' + str(count[3]) + ', [SSR]' + str(count[2]) + ', [SR]' + str(count[1]) + ', [R]' + str(count[0]) + ')')

    print('Loaded cards. (Japanese:' + str(len(mlg_all[0])) + ', Korea:' + str(len(mlg_all[1])) + ', China:' + str(len(mlg_all[2])) + ')')
    
    emb = discord.Embed(title='Pickup Cards')
    emb.add_field(name='Japanese:' + pickup_name[0], value=name[0])
    emb.add_field(name='Korean:' + pickup_name[1], value=name[1])
    emb.add_field(name='Chinese:' + pickup_name[2], value=name[2])

    if flag == 1: await msg.edit(content='All MLreload process completed successfully.', embed=emb)

    print(strtimestamp() + 'All MLreload process completed successfully.')
    print(strtimestamp() + '-----------------------------------------')

    return

async def gacha_note(message,langint):
    char_list = list()

    try:
        with open('./gacha/' + langnamelist[langint] + str(message.author.id) + '.txt', 'r') as f:
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
        for val in mlg_all[langint]:
            try:
                if char_list[val["id"]] == '1' and val["rarity"] == n:
                    cards.insert(0, val)
            except:
                pass

    for val in cards:
        if count == 10:
            text.append('')
            page += 1
            count = 0

        text[page] += '\n[' + rarity_str[val["rarity"]] + ']' + val["name"] + ' ' + val["idol"]
        count += 1

    gacha_count = str()
    try:
        with open('./gacha_count/' + langnamelist[langint] + str(message.author.id) + '.txt', 'r') as f:
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

async def mlg_touch(message,result,kind,vc,botmsg,langint):
    fes_flag = 0
    ssr_flag = 0
    sr_flag = 0
    author = message.author
    
    if kind == 'ミリオンフェス' or kind == '百萬祭典' or kind == '밀리언 페스티벌':
        for val in result:
            if val["rarity"] == 3:
                fes_flag = 1
                pink_flag = random.randint(1, 20)
                if pink_flag == 10:
                    img = 'https://i.imgur.com/fGpfCgB.gif'
                elif pink_flag == 20:
                    img = 'https://i.imgur.com/jWTTZ0d.gif'
                else:
                    img = 'https://i.imgur.com/0DxyVhm.gif'
                break
            elif val["rarity"] == 2:
                ssr_flag = 1
            elif val["rarity"] == 1:
                sr_flag = 1

        if not fes_flag == 1:
            if ssr_flag == 1:
                img = 'https://i.imgur.com/jWTTZ0d.gif'
            elif sr_flag == 1 and not ssr_flag == 1:
                img = 'https://i.imgur.com/vF7fDn3.gif'
            else:
                img = 'https://i.imgur.com/hEHa49X.gif'
    else:
        for val in result:
            if val["rarity"] == 2:
                ssr_flag = 1
                break
            if val["rarity"] == 1:
                sr_flag = 1

        if ssr_flag == 1:
            img = 'https://i.imgur.com/jWTTZ0d.gif'
        elif sr_flag == 1 and not ssr_flag == 1:
            img = 'https://i.imgur.com/vF7fDn3.gif'
        else:
            img = 'https://i.imgur.com/hEHa49X.gif'

    await asyncio.sleep(0.7)

    waitemb = discord.Embed()
    if fes_flag == 1 and pink_flag == 10: waitemb.set_image(url='https://i.imgur.com/ZC8JK9i.gif')
    else: waitemb.set_image(url='https://i.imgur.com/da2w9YS.gif')
    waitemb.set_footer(text=pickup_name[langint])
    msg = await message.channel.send(message.author.mention, embed=waitemb)
    await msg.add_reaction('👆')

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
                openemb.set_footer(text=kind)
                openemb.set_image(url=img)
                await msg.edit(embed=openemb)

                if not vc == None:
                    await asyncio.sleep(0.4)
                    if fes_flag == 1 and not pink_flag == 20:
                        vc.play(discord.FFmpegPCMAudio('./resources/open_fes.mp3'))
                    else:
                        vc.play(discord.FFmpegPCMAudio('./resources/open.mp3'))
                    while vc.is_playing():
                        await asyncio.sleep(1)
                else:
                    await asyncio.sleep(6)
                break

        while count < len(result):
            result_10 = result[count]
            if result_10["rarity"] == 3:
                player_show = discord.FFmpegPCMAudio('./resources/fes.mp3')
                await msg.clear_reactions()
            elif result_10["rarity"] == 2:
                player_show = discord.FFmpegPCMAudio('./resources/ssr.mp3')
                await msg.clear_reactions()
            elif result_10["rarity"] <= 1:
                player_show = discord.FFmpegPCMAudio('./resources/normal.mp3')

            desc = rarity_str[result_10["rarity"]] + '　' + result_10["name"] + '　' + result_10["idol"]
            mlgnormalemb = discord.Embed(title=desc, description='(CV.' + result_10["cv"] + ')', colour=int(result_10["color"], 0))

            footer_text = kind + ' ' + str((count + 1)) + '/' + str(len(result))
            mlgnormalemb.set_author(name=author.name, icon_url=author.avatar_url)
            mlgnormalemb.set_footer(text=footer_text)

            mlgnormalemb.set_image(url=result_10["image"])
            if not vc == None: vc.play(player_show)

            #カード表示（SSRの場合特訓前）
            await msg.edit(content=author.mention, embed=mlgnormalemb)

            if result_10["rarity"] >= 2:
                if not vc == None:
                    while vc.is_playing():
                        await asyncio.sleep(1)
                    vc.play(discord.FFmpegPCMAudio('./resources/ssr_talk.mp3'))

                line = result_10["ssrText"].replace("ProP", author.name + "P")
                mlgssremb = discord.Embed(title=desc, description='(CV.' + result_10["cv"] + ')', colour=int(result_10["color"], 0))
                mlgssremb.set_footer(text=footer_text, icon_url=author.avatar_url)
                mlgssremb.set_image(url=result_10["imageAwake"])

                await asyncio.sleep(4.2)
                await msg.edit(content=author.mention, embed=mlgssremb)
                await asyncio.sleep(3)
                await msg.edit(content=author.mention + ' ' + result_10["idol"] + '「' + line + '」', embed=mlgssremb)

            await msg.add_reaction('👆')
            await msg.add_reaction('⏭')
            while True:
                target_reaction2, user = await client.wait_for('reaction_add', timeout=timeout)

                if target_reaction2.emoji == '👆' and user == author:
                    if not vc == None and vc.is_playing(): vc.stop()
                    count += 1
                    log += '[' + rarity_str[result_10["rarity"]] + ']' + result_10["name"] + ' ' + result_10["idol"] + '\n'
                    if count == len(result):
                        if not vc == None:
                            if not bgm_id == 0:
                                await botmsg.add_reaction('⏹')
                            await vc.disconnect()
                        await msg.clear_reactions()
                        await msg.delete()

                        gacha_count = str()
                        try:
                            with open('./gacha_count/' + langnamelist[langint] + str(message.author.id) + '.txt', 'r') as f:
                                gacha_count = f.read()
                        except:
                            print(strtimestamp() + '[ERROR]Gacha count read FAILED.')

                        toLog = client.get_channel(log_id)
                        footer_text = kind
                        mlglogemb = discord.Embed(title=_('ガシャ結果'), description=log + '\n' + _('ドリームスター所持数：') + gacha_count)
                        mlglogemb.set_author(name=author.name, icon_url=author.avatar_url)
                        mlglogemb.set_footer(text=footer_text)
                        await toLog.send(embed=mlglogemb)

                        break
                    else:
                        await msg.remove_reaction(target_reaction2.emoji, user)
                    break
                elif target_reaction2.emoji == '⏭' and user == author and len(result) == 10:
                    for n,box in enumerate(result):
                        if count > n:
                            continue
                        log += '[' + rarity_str[box["rarity"]] + ']' + box["name"] + ' ' + box["idol"] + '\n'
                        if box["rarity"] >= 2:
                            ssr_skip.append(box)
                            ssr_count.append(str(n+1))

                    if len(ssr_skip) > 0:
                        for n,result_ssr in enumerate(ssr_skip):
                            if result_ssr["rarity"] == 3:
                                player_show = discord.FFmpegPCMAudio('./resources/fes.mp3')
                                await msg.clear_reactions()
                            elif result_ssr["rarity"] == 2:
                                player_show = discord.FFmpegPCMAudio('./resources/ssr.mp3')
                                await msg.clear_reactions()

                            desc = rarity_str[result_ssr["rarity"]] + '　' + result_ssr["name"] + '　' + result_ssr["idol"]
                            mlgnormalemb = discord.Embed(title=desc, description='(CV.' + result_ssr["cv"] + ')', colour=int(result_ssr["color"], 0))

                            footer_text = kind + ' ' + str(ssr_count[n]) + '/' + str(len(result))
                            mlgnormalemb.set_author(name=author.name, icon_url=author.avatar_url)
                            mlgnormalemb.set_footer(text=footer_text)

                            mlgnormalemb.set_image(url=result_ssr["image"])
                            if not vc == None and vc.is_playing():
                                vc.stop()
                                vc.play(player_show)

                            await msg.edit(content=author.mention, embed=mlgnormalemb)

                            if not vc == None:
                                while vc.is_playing():
                                    await asyncio.sleep(1)
                                vc.play(discord.FFmpegPCMAudio('./resources/ssr_talk.mp3'))

                            line = result_ssr["ssrText"].replace('ProP', author.name + 'P')
                            mlgssremb = discord.Embed(title=desc, description='(CV.' + result_ssr["cv"] + ')', colour=int(result_ssr["color"], 0))
                            mlgssremb.set_footer(text=footer_text, icon_url=author.avatar_url)
                            mlgssremb.set_image(url=result_ssr["imageAwake"])

                            await asyncio.sleep(4.2)
                            await msg.edit(content=author.mention, embed=mlgssremb)
                            await asyncio.sleep(3)
                            await msg.edit(content=author.mention + ' ' + result_ssr["idol"] + '「' + line + '」', embed=mlgssremb)

                            await msg.add_reaction('👆')
                            while True:
                                target_reaction2, user = await client.wait_for('reaction_add')

                                if target_reaction2.emoji == '👆' and user == author:
                                    if not vc == None and vc.is_playing(): vc.stop()
                                    count += 1
                                    await msg.remove_reaction(target_reaction2.emoji, user)
                                    break

                    if not vc == None:
                        if not bgm_id == 0:
                            await botmsg.add_reaction('⏹')
                        await vc.disconnect()

                    gacha_count = str()
                    try:
                        with open('./gacha_count/' + langnamelist[langint] + str(message.author.id) + '.txt', 'r') as f:
                            gacha_count = f.read()
                    except:
                        print(strtimestamp() + '[ERROR]Gacha count read FAILED.')

                    count += 10
                    await msg.delete()
                    toLog = client.get_channel(log_id)
                    footer_text = kind
                    mlglogemb = discord.Embed(title=_('ガシャ結果'), description=log + '\n' + _('ドリームスター所持数：') + gacha_count)
                    mlglogemb.set_author(name=author.name, icon_url=author.avatar_url)
                    mlglogemb.set_footer(text=footer_text)
                    await toLog.send(embed=mlglogemb)
                    break
        print(strtimestamp() + 'MLGacha complete. ' + author.name + '`s result\n' + log)
    except TimeoutError:
        await msg.delete()
        if not vc == None:
            await vc.disconnect()
        if not bgm_id == 0:
            await botmsg.add_reaction('⏹')
        await message.channel.send(_('しばらく操作がなかったため、タイムアウトしました。'))

def voicecheck():
    try:
        if not client.voice_clients[0] is None:
            return True
    except:
        return False

def pickupcheck(langint):
    global version, pickup_id
    name = ''
    for row in mlg_data[langint]:
        if row["id"] in pickup_id[langint]:
            lim = _('限定') if row["limited"] == True else ''
            name += '［' + lim + rarity_str[row["rarity"]] + '］' + row["name"] + ' ' + row["idol"] + ' (CV.' + row["cv"] + ')\n'
    print(name)
    return name

def langtoint():
    if lang == 'ja':
        return 0
    elif lang == 'kr':
        return 1
    elif lang == 'cn':
        return 2
    else:
        return 0

def langtostr(langint):
    if langint == 0:
        return 'ja'
    elif langint == 1:
        return 'kr'
    elif langint == 2:
        return 'cn'
    else:
        return 0

def langstrtoint(langstr):
    if 'ja' in langstr:
        return 0
    elif 'kr' in langstr:
        return 1
    elif 'cn' in langstr:
        return 2
    else:
        return 0

def strtimestamp():
    date = datetime.datetime.now()
    timestamp = '[' + str(date.year) + '-' + str(date.month) + '-' + str(date.day) + ' ' + str(date.hour) + ':' + str(date.minute) + ':' + str(date.second) + ']'
    return timestamp

client.run(token)