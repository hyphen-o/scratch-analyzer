import json
import requests
import csv

# 座標情報を格納しているキー名
MOVE = ['STEPS', 'DEGREES', 'DIRECTION', 'X', 'Y', 'DX', 'DY']
# 待機時間情報を格納しているキー名
WAIT = ['DURATION', 'SECS']


def toJson(project_id):
    # プロジェクトIDからScratchAPIを叩いてJson取得
    url = requests.get(
        f'https://api.scratch.mit.edu/projects/{project_id}')
    project_token = json.loads(url.text)['project_token']
    json_data = json.loads(requests.get(
        f'https://projects.scratch.mit.edu/{project_id}?token={project_token}').text)
    with open('project_json/Square.json', 'w') as f:
        json.dump(json_data, f, ensure_ascii=False)
    print(json_data)
    return json_data

# スクリプトの初めのブロックを出力


def writeBlocks(allblocks, block_hash, csv_name, field_name):
    block_name = allblocks[block_hash]['opcode']
    with open(f'out_csv/{csv_name}', 'a') as f:
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
        writeBlocks(allblocks, allblocks[block_hash]['next'], csv_name, None)


def writeEventBlock(allblocks, block_hash, csv_name):
    # 次のブロックがあるか確認
    if (allblocks[block_hash]['next'] != None):
        block_name = allblocks[block_hash]['opcode']
        # CSVファイルにブロック情報を書き込む
        with open(f'out_csv/{csv_name}', 'a') as f:
            writer = csv.writer(f)
            writer.writerow(['Nextscript', None, None])
            # 「キーを押した時ブロック」の時はキー情報も書き込む
            if (block_name == 'event_whenkeypressed'):
                key_name = allblocks[block_hash]['fields']['KEY_OPTION'][0]
                writer.writerow([block_name, key_name, None])
            else:
                writer.writerow([block_name, None, None])
        # 次のブロックを見る
        writeBlocks(allblocks, allblocks[block_hash]['next'], csv_name, None)


project_id = 747365086
json_data = toJson(project_id)
# スプライト1の全ブロック情報
allblocks = json_data['targets'][1]['blocks']
start_hash = ''

csv_name = f'{project_id}_sorted.csv'
with open(f'out_csv/{csv_name}', 'w') as f:
    writer = csv.writer(f)
    writer.writerow(['BlockName', 'Input', 'Movement'])

# 並列に存在するフラグブロックのハッシュ値の特定
i = 0
for k, v in allblocks.items():
    print('blockname: ' + v['opcode'])
    if ('event' in v['opcode']):
        print(v['opcode'])
        writeEventBlock(allblocks, k, csv_name)
        i += 1
