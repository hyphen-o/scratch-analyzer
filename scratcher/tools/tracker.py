import sys

sys.path.append("../")

from utils import DfManager
from config import constants

import math
import pandas as pd
import ast


class Tracker:
    """Scratch作品のスプライト動作軌跡を取得するためのクラス"""

    # 座標情報を格納しているキー名
    __MOVE = constants.MOVE_FIELDS
    __SET = constants.SET_FIELDS
    __DEGREE = constants.DEGREE_FIELDS
    # 待機時間情報を格納しているキー名
    __WAIT = constants.WAIT_FIELDS
    __COORDINATE = constants.COORDINATE_FIELDS

    def __init__(self, project):
        if isinstance(project, str):
            self.__sorted_df = pd.read_csv(project)
        elif isinstance(project, pd.DataFrame):
            self.__sorted_df = project
        else:
            print("プロジェクトへのパスか，プロジェクトを入力としてください．")
            return

        self.__dfM = DfManager(["key", "x", "y", "wait", "move_index"])

    def to_csv(self, dir_path):
        """時系列の座標情報をCSVに保存
        Args:
            dir_path(str): CSVを保存するパス（ファイル名含む）
        """
        self.__dfM.to_csv(dir_path)

    def __get_step_movement(self, steps):
        degree_rad = math.radians(90.0 - float(self.__degree))
        dx = steps * math.cos(degree_rad)
        dy = steps * math.sin(degree_rad)
        return (dx, dy)

    def get_coordinate(self):
        """ソートされたブロックからスプライトの動作軌跡を計算して取得
        Returns:
            Dataframe: 計算した動作軌跡のDataframeを返す
        """
        self.__degree = self.__sorted_df.iloc[0]["BlockName"]
        self.__x = self.__sorted_df.iloc[0]["Key"]
        self.__y = self.__sorted_df.iloc[0]["Field"]
        self.__df_length = len(self.__sorted_df.index)
        try:
            for i in range(1, self.__df_length):
                block_name = self.__sorted_df.iloc[i]["BlockName"]
                if block_name == "event_whenflagclicked":
                    self.__dfM.add_row([None, self.__x, self.__y, 0, i])
                    self.__calculate_coordinate(i)
                    break
            for i in range(1, self.__df_length):
                block_name = self.__sorted_df.iloc[i]["BlockName"]
                if "event" in str(block_name):
                    if block_name != "event_whenflagclicked":
                        self.__dfM.add_row([None, self.__x, self.__y, 0, i])
                        self.__calculate_coordinate(i)

            return self.__dfM.get_df()

        except Exception as e:
            print("error: " + str(e))

    def __calculate_coordinate(self, index):
        wait = 0.0
        for i in range(index, self.__df_length):
            try:
                if self.__sorted_df["BlockName"].iloc[i] == "SCRIPT":
                    return
                if not pd.isna(self.__sorted_df.iloc[i]["Field"]):
                    dic = ast.literal_eval(self.__sorted_df.iloc[i]["Field"])
                    for key in dic.keys():
                        if key in self.__MOVE:
                            if key == "DX":
                                self.__x = float(self.__x) + float(dic[key][1][1])
                            elif key == "DY":
                                self.__y = float(self.__y) + float(dic[key][1][1])
                        elif key in self.__SET:
                            if key == "X":
                                self.__x = float(dic[key][1][1])
                            elif key == "Y":
                                self.__y = float(dic[key][1][1])
                        elif key in self.__DEGREE:
                            if key == "DEGREES":
                                if (
                                    self.__sorted_df.iloc[i]["BlockName"]
                                    == "motion_turnleft"
                                ):
                                    self.__degree = float(self.__degree) + float(
                                        dic[key][1][1]
                                    )
                                elif (
                                    self.__sorted_df.iloc[i]["BlockName"]
                                    == "motion_turnright"
                                ):
                                    self.__degree = float(self.__degree) - float(
                                        dic[key][1][1]
                                    )
                            if key == "DIRECTION":
                                self.__degree = float(dic[key][1][1])
                        elif key == "STEPS":
                            result = self.__get_step_movement(float(dic[key][1][1]))
                            self.__x = float(self.__x) + result[0]
                            self.__y = float(self.__y) + result[1]
                        elif key in self.__WAIT:
                            wait += float(dic[key][1][1])
                    for string in self.__COORDINATE:
                        if string in dic:
                            self.__dfM.add_row([None, self.__x, self.__y, wait, i])
                            break
                    wait = 0.0
            except Exception as e:
                print(e)

        return
