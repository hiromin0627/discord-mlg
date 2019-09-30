# discord-mlg
PythonベースのDiscord用ボットのアイドルマスターミリオンライブシアターデイズのガシャシミュレーターです。  
現状、Discord.pyが音声を二重再生させることができない（わからない）ため、BGMを鳴らす場合は2つのボットを作成する必要がある。  

# MLG v2.2.0より新しいボットを使っている方へ
v2.2.0以降は以下のリンクからMLGデータベースを手動でダウンロード、更新してください！  
[DOWNLOAD MLG DATA](https://www.dropbox.com/sh/dph3omqrb0mn1y2/AAARp4G9iI6PaqmAYYGrW17xa?dl=0)  
**「gacha_data」**フォルダにダウンロードしたデータを**展開**してください。 
![Imgur](https://i.imgur.com/6bbbiVE.png)  
  
データベースの内容はこちらのWikiページを確認してください  
[Gacha data description](https://github.com/hiromin0627/discord-mlg/wiki/Gacha-data-description)  
  
## 導入方法
1. Python 3.7以降を導入してください。
1. 最新版のdiscord.py（v1.0.0以降）をインストールしてください。
1. ffmpegを導入し、PATHも通してください。
1. Discordのデベロッパーサイトからトークンを入手してください。
1. discord-mlgのconfig.iniにトークンとテキストチャンネルID（ガシャ結果ログ出力用）を入力してください。
    1. BGMも使う場合は、トークン（BGMボット用）とテキストチャンネルID（Bot同士の会話用）を用意、入力してください。
1. main.pyをPythonで起動します（Windowsだったらrun.batファイルを使用できます）。
    1. BGMを使用するならば、bgm.pyを起動します（Windowsならrun_bgm.batが使用できます）。
1. 素敵なガシャライフを！

## 遊び方
- 「MLガシャ」または「MLgacha」、「ML轉蛋」、「ML촬영」と入力するとミリシタのガシャを引くことができます。  
- 「MLガシャ10」または「MLgacha10」、「ML轉蛋10」、「ML촬영10」のように入力すると10連ガシャになります。
- 先頭語の「ML」はConfig.iniで変更できます。
  
## コマンド
- MLガシャ or MLgacha or ML轉蛋 or ML촬영 : ミリシタのガシャを引くことができます。 
- MLreload : ミリシタガシャのデータを変更した際、起動中にデータを入れ替えることができます。  
- MLreset : 全ユーザーのガシャのカウント（ドリームスター）の数をリセットできます。
- MLcard : ユーザーの持っているカードリストを確認できます。
- MLpickup : 現在のピックアップカードを確認できます。「cn」や「kr」などを言語省略語を入れると別の言語のガシャピックアップカードを確認できます。
- MLcall : カード名を入力することによってカード絵を確認できます。ただし、「シアターデイズ」と「制服シリーズ」はアイドル名も必要です。
  
### MLガシャのコマンドオプション  
- 「MLガシャ10」コマンドに「10」を追加すると10連ガシャがプレイできます。  
- 「MLガシャ」コマンドに「ja」か「cn」か「kr」を追加すると他の国のガシャをプレイできます（v2.0.0以降）。
- 「ja」が日本語、「cn」が中国語繁体字、「kr」が韓国語です。
- これらのオプションは「MLガシャ10cn」のように併用可能です。
  
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
### v2.2.1
- リロード時の文言を変更（完了時のメッセージの変更・完了時のピックアップカードの埋め込みにて限定の文字をローカライズ化）
- そもそも翻訳するだろうし結局READMEを日本語化

## 中国語繁体字版と韓国語版の記録データの互換性  
- 中国語繁体字版と韓国語版の記録データには互換性があります。
- ただし日本語版と中国語繁体字版と韓国語版の記録データには互換性がありませんので注意してください。
  
## 予定
- numpyを使用してリストの高速化を図れたらと思っている（インストール必須だからどうか考えてる）
- 韓国版や繁体字版の翻訳をしっかりする（セリフなど分かり次第翻訳）  
- config.iniで簡単に自分で確率をいじることができるようになったら面白そう  