import csv
import os
import json

csv_path= './available_blocks(3.0).csv'

ava_blocks = []
ds_cnt = 0
notds_cnt = 0

#フィルタリング用関数
def filterJson(block_hash):
    for k in block_hash:
        for block, ava in ava_blocks:
            if block_hash[k]['opcode'] == block and int(ava) == 0: 
                return False
    return True

#ファイルの読み込み，実行用関数
def separateJson(json_load, json_path):
    global ds_cnt
    global notds_cnt
    #フィルタリング用CSVの読み込み
    with open(csv_path, encoding = 'utf-8-sig') as f:
        reader = csv.reader(f)
        for row in reader:
            ava_blocks.append(row)
    #jsonファイルの読み込み
    block_hash = json_load['targets'][1]['blocks']
    if filterJson(block_hash):
        with open(f'./dataset_json/{json_path}', 'w') as f:
            json.dump(json_load, f, ensure_ascii=False)
        ds_cnt += 1
        print("dataset")
    else:
        with open(f'./notdataset_json/{json_path}', 'w') as f:
            json.dump(json_load, f, ensure_ascii=False)
        notds_cnt += 1
        print("not dataset")

default = 0

for filename in os.listdir("./inp-d_json"):
    try:
        with open(os.path.join("./inp-d_json", filename), 'r') as f:
            json_load = json.load(f)
            separateJson(json_load, filename)
    except:
        continue

print(ds_cnt)
print(notds_cnt)