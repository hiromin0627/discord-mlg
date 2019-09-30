# discord-mlg
PythonベースのDiscord用ボットのアイドルマスターミリオンライブシアターデイズのガシャシミュレーターです。  
現状、Discord.pyが音声を二重再生させることができない（わからない）ため、BGMを鳴らす場合は2つのボットを作成する必要がある。  

# for MLG v2.2.0 newer users
You need to prepare the MLG data yourself after MLG v2.2.0. Please download MLG data from my dropbox.  
（v2.2.0以降は以下のリンクからMLGデータベースを手動でダウンロード、更新してください！）  
<span style="font-size: 200%">[DOWNLOAD MLG DATA](https://www.dropbox.com/sh/dph3omqrb0mn1y2/AAARp4G9iI6PaqmAYYGrW17xa?dl=0)</span>  
Data is **placed in the “gacha_data”** directory.  
（**「gacha_data」**フォルダにダウンロードしたデータを**展開**してください。）  
[Imgur](https://imgur.com/6bbbiVE)
  
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
  
## What is new in MLG v2.0.0
- Config.iniの言語設定にかかわらず、別の国のガシャを引くことができるようになった。
- 言語別にガシャデータを管理するようになった（中国語繁体字版と韓国語版は統合してもいいかもしれないが、これからを考えて分離）。
- ピックアップ名を比較して、最新のガシャデータがある場合はダウンロードしなくなった。
- 変数が減ってしまった。そのかわり巨大なリストが誕生した。
- 一部翻訳を追加した。
- コンソール画面にてタイムスタンプが表示されるようになった（printでタイムスタンプ表記を追加した）。
### v2.0.1
- ピックアップ表示順をレア度の高い順になっていなかったのでレア度の高い順にしました。
- リリースには出してませんし、内部バージョン表記は2.0.0のままです。
### v2.1.0
- MLガシャを実行したユーザーがいるボイスチャンネルにボットが接続するようになりました。
- configでボイスチャンネルのIDを打つ必要がなくなりました。
### v2.2.0
- データベースをダウンロードする形式を**廃止**しました。
- データベースは[こちらのDropbox](https://www.dropbox.com/sh/dph3omqrb0mn1y2/AAARp4G9iI6PaqmAYYGrW17xa?dl=0)からダウンロードする形式にしました。
- ピックアップ確認時の画像を廃止しました。

## Info  
- Chinese gacha data and Korean gacha data are compatible. But Japanese gacha data and these gacha data are not compatible.  
  
## 予定
- numpyを使用してリストの高速化を図れたらと思っている（インストール必須だからどうか考えてる）
- 韓国版や繁体字版の翻訳をしっかりする（セリフなど分かり次第翻訳）  
- config.iniで簡単に自分で確率をいじることができるようになったら面白そう  