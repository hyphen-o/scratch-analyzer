import json
import requests
import csv


def toJson(project_id):
    # プロジェクトIDからScratchAPIを叩いてJson取得
    url = requests.get(
        f'https://api.scratch.mit.edu/projects/{project_id}')
    project_token = json.loads(url.text)['project_token']
    text = requests.get(
        f'https://projects.scratch.mit.edu/{project_id}?token={project_token}').text
    json_data = json.loads(text)
    with open('project_json/Square.json', 'w') as f:
        json.dump(json_data, f, ensure_ascii=False)
    return json_data

# スクリプトの初めのブロックを出力


def firstnode(allblocks, start_hash, i):
    if (allblocks[start_hash]['next'] != None):
        csv_name = 'SortedScripts[' + str(i) + '].csv'
        print(csv_name)
        # CSVファイルに書き込み
        with open(f'out_csv/{csv_name}', 'w') as f:
            writer = csv.writer(f)
            writer.writerow(['Blockname', 'Input', 'Move'])
            # フラグとしての入力ブロックの時，入力ブロックの種類を出力
            if (allblocks[start_hash]['opcode'] == 'event_whenkeypressed'):
                writer.writerow([allblocks[start_hash]['opcode'],
                                None, allblocks[start_hash]['fields']['KEY_OPTION'][0]])
            else:
                writer.writerow([allblocks[start_hash]['opcode'],
                                None, None])
        print(allblocks[start_hash]['opcode'])
        print(allblocks[start_hash]['inputs'])
        print(allblocks[start_hash]['fields'])
        nextblock(allblocks, allblocks[start_hash]
                  ['next'], csv_name, None)


def nextblock(blocks, hash, csv_name, fieldname):

    # CSVファイルに書き込み
    with open(f'out_csv/{csv_name}', 'a') as f:
        writer = csv.writer(f)
        flg = False
        if (fieldname):
            writer.writerow([blocks[hash]['opcode'], blocks[hash]
                            ['fields'][fieldname][0], None])
        else:
            if (blocks[hash]['inputs'] == "{{}}"):
                writer.writerow(
                    [blocks[hash]['opcode'], None, None])
            else:
                for k in blocks[hash]['inputs']:
                    if (k in MOVE or k in WAIT):
                        writer.writerow(
                            [blocks[hash]['opcode'], None, blocks[hash]['inputs']])
                        flg = True
                        break
                if not flg:
                    writer.writerow(
                        [blocks[hash]['opcode'], None, None])
    print(blocks[hash]['opcode'])
    print(blocks[hash]['inputs'])
    print(blocks[hash]['fields'])
    if (blocks[hash]['inputs'] != None):
        for k in blocks[hash]['inputs']:
            # 制御ブロックor条件付きブロックの場合その中身も見る
            if (k == 'SUBSTACK' or k == 'CONDITION'):
                nextblock(blocks, blocks[hash]['inputs']
                          [str(k)][1], csv_name, None)
            # 条件ブロックの中身を見る
            if (k == 'KEY_OPTION' and blocks[hash]['inputs']['KEY_OPTION'][1] != None):
                nextblock(blocks, blocks[hash]['inputs']
                          [str(k)][1], csv_name, k)
    # 次のブロックを見る
    if (blocks[hash]['next'] != None):
        nextblock(blocks, blocks[hash]['next'], csv_name, None)


project_id = 747365086
json_data = toJson(project_id)
# スプライト1の全ブロック情報
allblocks = json_data['targets'][1]['blocks']
start_hash = ''

# 座標情報を格納しているキー名
MOVE = ['STEPS', 'DEGREES', 'X', 'Y', 'DX', 'DY']
# 待機時間情報を格納しているキー名
WAIT = ['DURATION', 'SECS']

# 並列に存在するフラグブロックのハッシュ値の特定
i = 0
for k, v in allblocks.items():
    print(k)
    if ('event' in v['opcode']):
        firstnode(allblocks, k, i)
        i += 1
