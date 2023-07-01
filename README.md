## Scratch研究用ライブラリ
（ライブラリと同じ感覚で使用できることを目標としています）

## 本ライブラリを使う主な目的
* Scratchのデータをjson, csv形式で取得
* Scratchデータをより使いやすい形に変換
* Scratchデータを用いた類似度算出（DTWや編集距離）

## Setup
```git clone https://github.com/keigo-0314/scratch-analyzer.git```

※ ローカルで実行する方
1. `src`ディレクトリに移動
2. ```pip install requirements.txt```

※ Dockerで実行する方
1. ルートディレクトリへ移動して以下のコードを入力

```make up```

2. Pythonファイルを実行する場合は以下のコマンドでコンテナ内に入ってコマンド実行

```make exec```

## モジュールの解説（整理済みのモジュールのみ記載しています）
```src
├── api
│   ├── __init__.py
│   └── scratchApi.py #ScratchApiを叩くためのモジュール
├── app
│   └── ...　#内部で利用する場合は，このフォルダ内でファイルを作成してください
├── ast
│   └── ...
├── config
│   ├── command.txt
│   └── get-pip.py
├── dtw
│   ├── __init__.py
│   └── dtw.py #DTWを取得するためのモジュール
├── edit
│   └── ...
├── extracter
│   └── ...
├── snapshot
│   └── ...
├── spriteCoordinater
│   └── spriteCoordinate.py　#スプライトの座標取得プログラム
└── utils
    ├── __init__.py
    ├── dataset.py
    ├── drawGraph.py #図を描画するためのモジュール
    ├── manageFiles.py #ファイル管理するためのモジュール
    └── scratchManager.py #scratchプログラムを管理するためのモジュール
```
