import sys
import json
import os
import csv
import glob
from collections import Counter

sys.path.append("../../")

from api import scratch_client
from api import drscratch_analyzer
import prjman
from prjman import ProjectManager

def extract_ids_from_files(directory):
    """ディレクトリ内のJSONファイルからauthor ID、project ID、remix root IDを抽出
    Args:
        directory (str): JSONファイルが含まれるディレクトリのパス

    Returns:
        author ID、project ID、およびremix root IDのリスト
    """
    author_ids = []
    project_ids = []
    remix_root_ids = []

    file_pattern = os.path.join(directory, '*.json')

    for file_path in glob.glob(file_pattern):
        if os.path.isfile(file_path):
            try:
                with open(file_path, 'r') as file:
                    data = json.load(file)
                    if isinstance(data, list):
                        for project in data:
                            if (
                                "author" in project and
                                "id" in project and
                                "id" in project["author"] and
                                isinstance(project["author"]["id"], int) and
                                isinstance(project["id"], int) and
                                project["id"] > 276751787 and
                                "remix" in project and
                                "root" in project["remix"] and
                                isinstance(project["remix"]["root"], int)
                            ):
                                author_ids.append(project["author"]["id"])
                                project_ids.append(project["id"])
                                remix_root_ids.append(project["remix"]["root"])
                    else:
                        print(f"ファイルのデータ形式が予期しない形式: {file_path}")
            except json.JSONDecodeError:
                print(f"JSONのデコードエラーが発生: {file_path}")
            except Exception as e:
                print(f"ファイルの読み込み中にエラーが発生 {file_path}: {e}")

    if not author_ids or not project_ids or not remix_root_ids:
        print("指定されたディレクトリには有効なデータがない")

    return author_ids, project_ids, remix_root_ids

def extract_metrics(project_ids, author_ids, remix_root_ids):
    """ScratchプロジェクトIDのリストからメトリクスを抽出

    Args:
        project_ids (list): ScratchプロジェクトIDのリスト
        author_ids (list): プロジェクトIDに対応するauthorIDのリスト
        remix_root_ids (list): プロジェクトIDに対応するremixrootIDのリスト

    Returns:
        tuple: ブロックの長さ、ブロックタイプの長さ、およびスプライトの長さのリスト
    """
    blocks_lengths = []
    block_types_lengths = []
    sprites_lengths = []

    i = 0
    while i < len(project_ids):
        try:
            project_id = project_ids[i]
            project_manager = ProjectManager(project_id)
            blocks_lengths.append(project_manager.get_all_blocks_length())
            block_types_lengths.append(project_manager.get_blocks_type_length())
            sprites_lengths.append(project_manager.get_sprites_length())
            print("blocks count = " + str(blocks_lengths[-1]))
            print("blockType = " + str(block_types_lengths[-1]))
            print("sprites count = " + str(sprites_lengths[-1]))
            i += 1
        except IndexError:
            print(f"プロジェクトID {project_id} の処理中にインデックスエラーが発生　リストから削除")
            del project_ids[i]
            del author_ids[i]
            del remix_root_ids[i]
        except Exception as e:
            print(f"プロジェクトID {project_id} の処理中にエラーが発生: {e}")
            i += 1

    return blocks_lengths.copy(), block_types_lengths.copy(), sprites_lengths.copy()

def save_project_json(project_ids, directory):
    """プロジェクトJSONをファイルに保存

    Args:
        project_id (int): プロジェクトID
        directory (str): 保存先ディレクトリのパス
    """
    i = 0
    while i < len(project_ids):
        project_id = project_ids[i]
        project_json = scratch_client.get_project(project_id)
        if project_json:
            file_path = os.path.join(directory, f"{project_id}.json")
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(project_json, f, ensure_ascii=False, indent=4)
                print(f"プロジェクトID {project_id} のJSONを {file_path} に保存")
                i += 1
            except Exception as e:
                print(f"プロジェクトID {project_id} のJSONを保存中にエラー発生")
                print(e)
                i += 1
        else:
            print(f"プロジェクトID {project_id} のJSONを取得不可")
            print(f"プロジェクトID {project_id} の処理中にインデックスエラーが発生　リストから削除")
            del project_ids[i]
            del author_ids[i]
            del remix_root_ids[i]
        

# 使用例
directory = '../../dataset/sample_projects'
author_ids, project_ids, remix_root_ids = extract_ids_from_files(directory)
blocks_lengths, block_types_lengths, sprites_lengths = extract_metrics(project_ids, author_ids, remix_root_ids)

# # 作品をjsonファイルに保存
# save_directory = '../../dataset/projects_json'
# save_project_json(project_ids, save_directory)

# # メトリクス抽出
# def extract_metrics(project_ids):
#     blocks_lengths = []
#     block_types_lengths = []
#     sprites_lengths = []

#     for project_id in project_ids:
#         project_manager = ProjectManager(project_id)
#         blocks_lengths.append(project_manager.get_all_blocks_length())
#         block_types_lengths.append(project_manager.get_blocks_type_length())
#         sprites_lengths.append(project_manager.get_sprites_length())
#         print("blocks count = " + str(blocks_lengths[-1]))
#         print("blockType =" + str(block_types_lengths[-1]))
#         print("sprites count = " + str(sprites_lengths[-1]))
#     return blocks_lengths.copy(), block_types_lengths.copy(), sprites_lengths.copy()

# csvに保存
def save_to_csv(author_ids, project_ids, blocks_lengths, block_types_lengths, sprites_lengths, ct_score, output_file):
    with open(output_file, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['Author_ID', 'Project_ID', 'remix_root_ID', 'Blocks_length', 'BlockType_length', 'Sprites_length'])  # ヘッダー行を書き込む
        for author_id, project_id, remix_root_id, blocks_length, block_types_length, sprites_length in zip(author_ids, project_ids, remix_root_ids, blocks_lengths, block_types_lengths, sprites_lengths):
            csvwriter.writerow([author_id, project_id, remix_root_id, blocks_length, block_types_length, sprites_length])

# # 使用例
# directory = '../../dataset/sample_projects'  # JSONファイルが格納されているディレクトリのパス
# author_ids, project_ids, remix_root_ids = extract_ids_from_files(directory)
# blocks_lengths, block_types_lengths, sprites_lengths = extract_metrics(project_ids)

# print("Author IDs:", author_ids)
# print("author IDs len:", len(author_ids))
# print("Project IDs:", project_ids)
# print("Project IDs len:", len(project_ids))
# print("Remix Root IDs:", remix_root_ids)
# print("Remix Root IDs len:", len(remix_root_ids))

# print("B : ", len(blocks_lengths))
# print("BT : ", len(block_types_lengths))
# print("S : ", len(sprites_lengths))

# # # サンプルプロジェクト
# sample_id = 797975999

# for project_id in project_ids:
#     print(project_id)
# print(len(project_ids))

# print(len(blocks_lengths))
# print(len(block_types_lengths))
# print(len(sprites_lengths))

# if not (len(author_ids) == len(project_ids) == len(blocks_lengths) == len(block_types_lengths) == len(sprites_lengths)):
#     print("Error: Lists have different lengths")
#     print(f"author_ids: {len(author_ids)}, project_ids: {len(project_ids)}, blocks_lengths: {len(blocks_lengths)}, block_types_lengths: {len(block_types_lengths)}, sprites_lengths: {len(sprites_lengths)}")
# else:
#     output_file = 'output.csv'
#     save_to_csv(author_ids, project_ids, blocks_lengths, block_types_lengths, sprites_lengths, output_file)
#     print("Data saved to", output_file)

# for id in project_ids:

#     # # ブロック数を取得
#     project_manager = ProjectManager(id)
#     # print("instance")
#     blocks_length = project_manager.get_all_blocks_length()

#     # # ブロックを取得
#     blockType_length = project_manager.get_blocks_type_length()

#     # # スプライト数を取得 "isStage"の数がスプライト数？1つはステージなので-1する
#     sprites_length = project_manager.get_sprites_length()

#     # # # CTスコア合計点数を取得
#     # mastery = drscratch_analyzer.Mastery()
#     # mastery.process("../../sample_json/797975999.json")
#     # mastery.analyze("./out.json")

#     with open('out.json', 'r', encoding='utf-8') as file:
#         data = json.load(file)
#     # # CTScoreの値をint型の変数に格納
#     ct_score = data["CTScore"]

    # # 出力
    # print("blocks count = " + str(blocks_length))
    # print("blockType =" + str(blockType_length))
    # print("sprites count = " + str(sprites_length))
    # print("CTscore = " + str(ct_score))


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