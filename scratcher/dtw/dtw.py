import sys
import csv
import os

sys.path.append('../')

import numpy as np
from tslearn.preprocessing import TimeSeriesScalerMinMax
from tslearn.utils import to_time_series_dataset

from utils import DfManager

class DTW:
    def __init__(self, windowSize=False):
        self.__windowSize = windowSize

    def setData(self, data1, data2):
        self.__data1 = self.__load_coordinate(data1)
        self.__data2 = self.__load_coordinate(data2)

    def getDtw(self, data_path=''): 
        if self.__windowSize:
            result = self.__calculatePartialDtw(self.__data1, self.__data2)
            return result
        else:
            dtwVal = self.__calculateDtw(self.__data1, self.__data2)[1]
            return dtwVal
                    

    def __calculatePartialDtw(self, data1, data2):
        try:
            if len(data1) < self.__windowSize or len(data2) < self.__windowSize:
                print("ウインドウサイズがデータサイズよりも大きいです")
                return None

            minDtwValue = float('inf')
            minRange1 = ""
            minRange2 = ""

            dfM = DfManager(f'../out/coordinate_final/{self.__key1}.csv')
            dfM2 = DfManager(f'../out/coordinate_final/{self.__key2}.csv')
            df = dfM.get_df()
            df2 = dfM2.get_df()

            for i in range(len(data1)):
                if i + self.__windowSize - 1 > len(data1):
                    break
                for j in range(len(data2)):
                    if j + self.__windowSize - 1 > len(data2):
                        break
                    data1 = data1[i: i + self.__windowSize - 1]
                    data2 = data2[j: j + self.__windowSize - 1]

                    dtwVal = self.__calculateDtw(data1, data2)[1]
                    if dtwVal <= minDtwValue:
                        minDtwValue = dtwVal

                        minRange1 = [df.iloc[i]['move_index'], df.iloc[i + self.__windowSize - 1]['move_index']]
                        minRange2 = [df2.iloc[j]['move_index'], df2.iloc[j + self.__windowSize - 1]['move_index']]
        except Exception as e:
            print(e)

        return minDtwValue, minRange1, minRange2

    def __load_coordinate(self, data):
        """
            data = [
                [x, y],
                [x1, x2],
                ...
            ]
        """

        return TimeSeriesScalerMinMax().fit_transform(
            to_time_series_dataset([data])).flatten().reshape(-1, 2)

    def __calculateDtw(self, x, y):
        # xのデータ数，yのデータ数をそれぞれTx,Tyに代入
        Tx = len(x)
        Ty = len(y)

        # C:各マスの累積コスト，　B：最小コストの行/列番号
        C = np.zeros((Tx, Ty))
        B = np.zeros((Tx, Ty, 2), int)

        # 一番初めのマスのコストを，xとyのそれぞれ一番初めの値にする
        C[0, 0] = self.__calculateDist(x[0], y[0])

        # 動的計画法を用いる
        # 左下のマスからスタートし，各マスに到達するため最小の累積コストを1マスずつ求める

        # 境界条件：両端が左下と右上にあること
        # 単調性：左下から始まり，右，上，右上のいずれかにしか進まないこと
        # 連続性：繋がっていること

        # 一番下の行は，真っ直ぐ右にコストが累積される
        for i in range(Tx):
            C[i, 0] = C[i - 1, 0] + self.__calculateDist(x[i], y[0])
            B[i, 0] = [i - 1, 0]

        # 同様に一番左の列は，真っ直ぐ上にコストが累積される
        for j in range(1, Ty):
            C[0, j] = C[0, j - 1] + self.__calculateDist(x[0], y[j])
            B[0, j] = [0, j - 1]

        # その他のマスの累積コストを求める
        for i in range(1, Tx):
            for j in range(1, Ty):
                pi, pj, m = self.__getMin(C[i - 1, j],
                                          C[i, j - 1],
                                          C[i - 1, j - 1],
                                          i, j)
                # get_minで返ってきた最小コストを累積コストに足す
                C[i, j] = self.__calculateDist(x[i], y[j]) + m
                # get_minで返ってきた最小コストの行/列番号を保持
                B[i, j] = [pi, pj]
        # 最終的な右上（最終の到達点）のコスト
        cost = C[-1, -1]

        path = [[Tx - 1, Ty - 1]]

        # 逆順にたどることでパスを求める
        i = Tx - 1
        j = Ty - 1

        while ((B[i, j][0] != 0) or (B[i, j][1] != 0)):
            path.append(B[i, j])
            i, j = B[i, j].astype(int)
        path.append([0, 0])
        return np.array(path), cost, C

    # 距離算出
    def __calculateDist(self, a, b):
        return ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** 0.5

    # 最小値算出
    def __getMin(self, m0, m1, m2, i, j):
        if m0 < m1:
            if m0 < m2:
                return i - 1, j, m0
            else:
                return i - 1, j - 1, m2
        else:
            if m1 < m2:
                return i, j - 1, m1
            else:
                return i - 1, j - 1, m2
