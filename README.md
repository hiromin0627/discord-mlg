# discord-mlg
PythonベースのDiscord用ボットのアイドルマスターミリオンライブシアターデイズのガシャシミュレーターです。  
現状、Discord.pyが音声を二重再生させることができない（わからない）ため、BGMを鳴らす場合は2つのボットを作成する必要がある。

## 予定
・韓国版や繁体字版のミリシタが登場したため、多言語対応させる（v1.1.0にて対応）
・自分でCSVを作成してオリジナルのガシャシミュレーターにできるといいな（MLGじゃなくなる）  
・config.iniで簡単に自分で確率をいじることができるようになったら面白そう  
・現在、BGM以外のすべての機能がmain.pyに収められているが、コマンドごとにモジュールを作成する（保留）  