# discord-mlg
PythonベースのDiscord用ボットのアイドルマスターミリオンライブシアターデイズのガシャシミュレーターです。  
現状、Discord.pyが音声を二重再生させることができない（わからない）ため、BGMを鳴らす場合は2つのボットを作成する必要がある。  
  
## 遊び方(How to play)
Type "MLgacha" or "MLガシャ" or "ML轉蛋" or "ML촬영" to play Million Live! Theater Days gacha.  
Add "10" (ex."MLgacha10") to play it for 10 times(10連ガシャ).
"ML" is prefix. So you can change at "config.ini".  
  
### コマンド(Commands)
- MLガシャ or MLgacha or ML轉蛋 or ML촬영 : Play IDOLM@STER Million Live! Theater Days gacha simulator.  
- MLreload : Download latest database.  
- MLreset : Clear users play count data.  
- MLcard : Check cards you have.  
- MLpickup : Check pickup cards.  
- MLcall : Check your cards for type card name(only you have).  
  
## Info  
- Chinese gacha data and Korean gacha data are compatible. But Japanese gacha data and these gacha data are not compatible.  
  
## 予定
- 韓国版や繁体字版のミリシタが登場したため、多言語対応させる（v1.1.0にて対応）  
- 韓国版や繁体字版の翻訳をしっかりする（セリフなど分かり次第翻訳）  
- 自分でCSVを作成してオリジナルのガシャシミュレーターにできるといいな（MLGじゃなくなる）  
- config.iniで簡単に自分で確率をいじることができるようになったら面白そう  
- 現在、BGM以外のすべての機能がmain.pyに収められているが、コマンドごとにモジュールを作成する（保留）  