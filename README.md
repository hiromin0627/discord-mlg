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
  
### Options for MLgacha  
- Add '10' for 'MLgacha' command, 'MLgacha10' for example. You can play MLG for 10 times(「MLガシャ10」コマンドに「10」を追加すると10連ガシャがプレイできます).  
- Add 'ja' or 'cn' or 'kr' for 'MLgacha' command, 'MLgachaja' for example. You can play other country MLG(「MLガシャ」コマンドに「ja」か「cn」か「kr」を追加すると他の国のガシャをプレイできます).
- 'ja' is Japanese, 'cn' is Chinese, and 'kr' is Korean(「ja」が日本語、「cn」が中国語繁体字、「kr」が韓国語です).
- Can be used together '10' and 'ja' or 'cn' or 'kr'. For example, 'MLgahca10cn'(これらのオプションは「MLガシャ10cn」のように併用可能です).
  
## What is new in MLGv2.0.0
- Config.iniの言語設定にかかわらず、別の国のガシャを引くことができるようになった。
- 言語別にガシャデータを管理するようになった（中国語繁体字版と韓国語版は統合してもいいかもしれないが、これからを考えて分離）。
- ピックアップ名を比較して、最新のガシャデータがある場合はダウンロードしなくなった。
- 変数が減ってしまった。そのかわり巨大なリストが誕生した。
- 一部翻訳を追加した。
- コンソール画面にてタイムスタンプが表示されるようになった（printでタイムスタンプ表記を追加した）。

## Info  
- Chinese gacha data and Korean gacha data are compatible. But Japanese gacha data and these gacha data are not compatible.  
  
## 予定
- numpyを使用してリストの高速化を図れたらと思っている（インストール必須だからどうか考えてる）
- 韓国版や繁体字版の翻訳をしっかりする（セリフなど分かり次第翻訳）  
- config.iniで簡単に自分で確率をいじることができるようになったら面白そう  