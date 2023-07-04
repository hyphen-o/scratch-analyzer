## Scratch 研究用ライブラリ

（ライブラリと同じ感覚で使用できることを目標としています）

## 本ライブラリを使う主な目的

- Scratch のデータを json, csv 形式で取得
- Scratch データをより使いやすい形に変換
- Scratch データを用いた類似度算出（DTW や編集距離）

## Setup

`git clone https://github.com/keigo-0314/scratch-analyzer.git`

**ローカルで実行する**

※Mac の方

1. インストールしたプロジェクトのルートディレクトリに移動
2. `make build`

※Windows の方

1. インストールしたプロジェクトのルートディレクトリに移動
2. `pip install setuptools wheel`
3. `python setup.py sdist bdist_wheel`

※共通

- どちらの場合も上記のコマンドを実行すると，ルートディレクト内に`dist`ディレクトリが作成される．
- パッケージをインストールする際は，

`pip install {このプロジェクトまでのPATH}/dist/scratcher-{dist内のバージョン参照}.tar.gz`

- 将来的には

**Docker で実行する**

1. インストールしたプロジェクトのルートディレクトリに移動
2. `make up`
3. `make exec`

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
    ├── util.py #汎用関数
    ├── dataset.py #データセット整形用モジュール
    ├── drawGraph.py #図を描画するためのモジュール
    ├── manageFiles.py #ファイル管理するためのモジュール
    └── pm.py #scratchプログラムを管理するためのモジュール
```
