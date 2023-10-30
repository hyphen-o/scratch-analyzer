"""
ブロック構造をASTに変換する
（引数ブロックなどへは未対応）
"""
import json
import sys
import uuid

import pandas as pd
import requests


class CodeToASTNode:
    c_blocks = [
        "control_repeat",
        "control_forever",
        "control_if",
        "control_if_else",
        "control_repeat_until",
        "control_all_at_once",
        "control_while",
        "control_for_each",
    ]

    def __init__(self, json_blocks):
        self.node_id = 0
        self.json_blocks = json_blocks
        self.df_script = pd.DataFrame(
            [["SCRIPT", 0, -1]], columns=["block", "node_id", "parent_node_id"]
        )  # 記録用のデータフレーム

    def get_result(self):
        return self.df_script

    def add_df(self, block, node_id, parent_node_id):
        se_add = pd.Series(
            [block, node_id, parent_node_id], index=self.df_script.columns
        )
        self.df_script = self.df_script.append(se_add, ignore_index=True)

    def depth_first_search(self, node_hash, parent_node_id):
        """
        深さ優先探索でノードを調べる
        """
        self.node_id += 1
        block = self.json_blocks[node_hash]["opcode"]  # ブロック名

        # 記録用のデータフレームにノード情報を追加する
        self.add_df(block, self.node_id, parent_node_id)

        # Cブロックについての処理
        if block in self.c_blocks:
            # if-elseブロックは2段階構造のため，処理を分ける
            if block == "control_if_else":
                current_node_id = self.node_id
                for key in ["SUBSTACK", "SUBSTACK2"]:
                    self.node_id += 1
                    self.add_df("SUBSTACK", self.node_id, current_node_id)
                    if key in self.json_blocks[node_hash]["inputs"]:
                        self.depth_first_search(
                            self.json_blocks[node_hash]["inputs"][key][1], self.node_id
                        )
            else:
                if "SUBSTACK" in self.json_blocks[node_hash]["inputs"]:
                    self.depth_first_search(
                        self.json_blocks[node_hash]["inputs"]["SUBSTACK"][1],
                        self.node_id,
                    )

        if self.json_blocks[node_hash]["next"] == None:
            return
        else:
            self.depth_first_search(self.json_blocks[node_hash]["next"], parent_node_id)


if __name__ == "__main__":
    if sys.argv[1] == "-r":
        if len(sys.argv) < 2:
            print(
                """
                作品IDと書き込み先のファイルパスを指定してください
                例. $python3 scratch_code_to_ast.py -r 619086872 ./out.csv
                """
            )
        else:
            project_id = sys.argv[2]
            write_path = sys.argv[3]  # 書き出し用のファイルパス
            random_string = uuid.uuid4().hex
            url = requests.get(
                f"https://projects.scratch.mit.edu/{project_id}/get?foo={random_string}"
            )

            try:
                print(url.text)
                json_data = json.loads(url.text)
            except json.JSONDecodeError as e:
                print(e)
                print("jsonデータの取得に失敗")
                exit()

            if "code" in json_data.keys():
                if json_data["code"] == "NotFound":
                    print("jsonデータの中身が空です")
                    exit()
    elif sys.argv[1] == "-f":
        if len(sys.argv) < 2:
            print(
                """
                読み込むjsonファイルパスと書き込み先のファイルパス，project_idを指定してください
                例. $python3 scratch_code_to_ast.py -r ./project.json ./out.csv 8392890483
                """
            )
        else:
            read_path = sys.argv[2]
            write_path = sys.argv[3]
            project_id = sys.argv[4]

            try:
                json_data = json.load(open(read_path))
            except json.JSONDecodeError as e:
                print("jsonデータの取得に失敗")
                exit()

    if "code" in json_data.keys():
        if json_data["code"] == "NotFound":
            print("jsonデータの中身が空です")
            exit()

    try:
        list_df = []
        script_id = 0
        for sprite_data in json_data["targets"]:
            sprite_name = sprite_data["name"]
            json_blocks = sprite_data["blocks"]
            if sprite_name != "Stage":
                for k, v in json_blocks.items():
                    if v["topLevel"] == True:
                        cta = CodeToASTNode(json_blocks=json_blocks)
                        cta.depth_first_search(node_hash=k, parent_node_id=0)
                        script_df = cta.get_result()
                        script_df["script_id"] = script_id
                        script_df["sprite_name"] = sprite_name
                        list_df.append(script_df)
                        script_id += 1
                        break
                break
            else:
                continue

        # 結果の出力
        df_concat = pd.concat(list_df)
        df_concat["project_id"] = project_id
        df_concat.to_csv(write_path, index=False)
    except:
        print("ID:{}の解析中にエラー発生".format(project_id))

        import traceback

        traceback.print_exc()
