import sys
import json
import os
import csv
from collections import Counter

sys.path.append("../../")

from api import scratch_client
from api import drscratch_analyzer
import prjman
from prjman import ProjectManager

# # サンプルプロジェクト
sample_id = 797975999

# # ブロック数を取得
project_manager = ProjectManager(sample_id)
# print("instance")
blocks_length = project_manager.get_all_blocks_length()

# # ブロックを取得
blockType_length = project_manager.get_blocks_type_length()

# # スプライト数を取得 "isStage"の数がスプライト数？1つはステージなので-1する
sprits_length = project_manager.get_sprites_length()

# # CTスコア合計点数を取得
mastery = drscratch_analyzer.Mastery()
mastery.process("../../sample_json/797975999.json")
mastery.analyze("./out.json")

with open('out.json', 'r', encoding='utf-8') as file:
    data = json.load(file)
# # CTScoreの値をint型の変数に格納
ct_score = data["CTScore"]

# # 出力
print("blocks count = " + str(blocks_length))
print("blockType =" + str(blockType_length))
print("sprites count = " + str(sprits_length))
print("CTscore = " + str(ct_score))

# # csvに保存

data = [
    [blocks_length, blockType_length, sprits_length, ct_score]
]

# ヘッダー
header = ["blocks_length", "blockType_length", "sprits_length", "CTscore"]

with open('example.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)

    writer.writerow(header)
    writer.writerows(data)

print("csv data update")



# プロジェクトの大元のリミックス元とそこから何回派生しているか
# PM = scratch_client.get_remix_parent(sample_id2)
# if PM:
#     # print("parent_id: " + str(PM["parent_id"]))
#     # print("deep: " + str(PM["deep"]))
#     with open('data/test_PM_' + str(sample_id2) + '.json', 'w') as f:
#         json.dump(str(PM), f, indent=2)

# print("metaData: " + str(MD))
# jsonファイルに出力
# with open('data/test_MD_' + str(sample_id2) + '.json', 'w') as f:
#     json.dump(str(MD), f, indent=2)

# リミックスしていたら1個前のプロジェクトのID出力
# parentが1個前
# if MD["remix"]["parent"]:
#     # print("parent_id: " + str(MD["remix"]["parent"]))
#     with open('data/test_MD_' + str(sample_id2) + '.json', 'w') as f:
#         json.dump(str(MD["remix"]["parent"]), f, indent=2)