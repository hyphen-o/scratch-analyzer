import json
import requests
import csv


def toJson(project_id):
    with open(f'project_json/{project_id}.json') as f:
        json_data = json.load(f)

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


project_id1 = 797975999
project_id2 = 112717508
json_data1 = toJson(project_id1)
json_data2 = toJson(project_id2)

allblocks2 = json_data2['children'][0]['scripts']


allblocks1 = json_data1['targets'][1]['blocks']
i = 0
for k, v in allblocks1.items():
    print('"' + str(allblocks2[i][2][0][0]) + '"' + ' : ' +
          '"' + v['opcode'] + '",')
    i += 1

# # スプライト1の全ブロック情報
# allblocks = json_data['targets'][1]['blocks']
# start_hash = ''

# csv_name = f'{project_id}_sorted.csv'
# with open(f'out_csv/{csv_name}', 'w') as f:
#     writer = csv.writer(f)
#     writer.writerow(['BlockName', 'Input', 'Movement'])

# # 並列に存在するフラグブロックのハッシュ値の特定
# i = 0
# for k, v in allblocks.items():
#     print('blockname: ' + v['opcode'])
#     if ('event' in v['opcode']):
#         print(v['opcode'])
#         writeEventBlock(allblocks, k, csv_name)
#         i += 1
