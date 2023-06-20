import json
import requests
import csv
import pandas as pd

# 座標情報を格納しているキー名
MOVE = ['STEPS', 'DEGREES', 'DIRECTION', 'X', 'Y', 'DX', 'DY']
# 待機時間情報を格納しているキー名
WAIT = ['DURATION', 'SECS']


def toJson(project_id):
    # プロジェクトIDからScratchAPIを叩いてJson取得
    try:
        url = requests.get(
            f'https://api.scratch.mit.edu/projects/{project_id}')
        project_token = json.loads(url.text)['project_token']
        json_data = json.loads(requests.get(
            f'https://projects.scratch.mit.edu/{project_id}?token={project_token}').text)
        return json_data
    except Exception as e:
        print(e)

# スクリプトの初めのブロックを出力


def writeBlocks(allblocks, block_hash, csv_name, field_name):
    try:
        block_name = allblocks[block_hash]['opcode']
        with open(f'sorted_csv/{csv_name}', 'a') as f:
            writer = csv.writer(f)
            flg = False
            if (field_name):
                writer.writerow([block_name, allblocks[block_hash]
                                ['fields'][field_name][0], None])
            else:
                if (allblocks[block_hash]['inputs'] == "{{}}"):
                    writer.writerow(
                        [block_name, None, None])
                else:
                    for key in allblocks[block_hash]['inputs']:
                        if (key in MOVE or key in WAIT):
                            writer.writerow(
                                [block_name, None, allblocks[block_hash]['inputs']])
                            flg = True
                            break
                    if not flg:
                        writer.writerow(
                            [block_name, None, None])
        if (allblocks[block_hash]['inputs'] != None):
            for key in allblocks[block_hash]['inputs']:
                # 制御ブロックor条件付きブロックの場合その中身も見る
                if (key == 'SUBSTACK' or key == 'CONDITION'):
                    writeBlocks(
                        allblocks, allblocks[block_hash]['inputs'][str(key)][1], csv_name, None)
                # 条件ブロックの中身を見る
                if (key == 'KEY_OPTION' and allblocks[block_hash]['inputs']['KEY_OPTION'][1] != None):
                    writeBlocks(
                        allblocks, allblocks[block_hash]['inputs'][str(key)][1], csv_name, key)
        # 次のブロックを見る
        if (allblocks[block_hash]['next'] != None):
            writeBlocks(
                allblocks, allblocks[block_hash]['next'], csv_name, None)
    except Exception as e:
        print(e)


def writeEventBlock(allblocks, block_hash, csv_name):
    # 次のブロックがあるか確認
    try:
        if (allblocks[block_hash]['next'] != None):
            block_name = allblocks[block_hash]['opcode']
            # CSVファイルにブロック情報を書き込む
            with open(f'sorted_csv/{csv_name}', 'a') as f:
                writer = csv.writer(f)
                writer.writerow(['Nextscript', None, None])
                # 「キーを押した時ブロック」の時はキー情報も書き込む
                if (block_name == 'event_whenkeypressed'):
                    key_name = allblocks[block_hash]['fields']['KEY_OPTION'][0]
                    writer.writerow([block_name, key_name, None])
                else:
                    writer.writerow([block_name, None, None])
            # 次のブロックを見る
            writeBlocks(
                allblocks, allblocks[block_hash]['next'], csv_name, None)
    except Exception as e:
        print(e)


def main(project_id):
    try:
        json_data = toJson(project_id)
        allblocks = json_data['targets'][1]['blocks']
        csv_name = f'{project_id}_sorted.csv'
        with open(f'sorted_csv/{csv_name}', 'w') as f:
            writer = csv.writer(f)
            writer.writerow(['Blockname', 'Key', 'Field'])
            writer.writerow([json_data['targets'][1]['direction'], json_data['targets'][1]
                            ['x'], json_data['targets'][1]['y']])

        # 並列に存在するフラグブロックのハッシュ値の特定
        for k, v in allblocks.items():
            if ('event' in v['opcode']):
                writeEventBlock(allblocks, k, csv_name)
    except Exception as e:
        print(e)


dataset_csv = pd.read_csv('out_csv/dataset_id.csv')
for i in range(len(dataset_csv.index)):
    project_id = dataset_csv.iloc[i][0]
    main(project_id)
    print(i)
