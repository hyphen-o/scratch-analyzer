import os
import pandas as pd
from tslearn.preprocessing import TimeSeriesScalerMinMax
from tslearn.utils import to_time_series_dataset


def loadCoordinate(data_path):
    dir_size = 0
    splittedData = []
    normalizedData = []

    print(data_path)
    # 検索対象ファイルの数確認
    for currentDir, dirs, fileNames in os.walk(data_path):
        print(fileNames)
        dir_size = len(fileNames)
        for fileName in fileNames:
            if fileName.startswith("."):
                dir_size -= 1

    # 1動作のcsvを読み込み，配列に保持（配列のインデックス=動作番号）
    for i in range(dir_size):
        data = pd.read_csv(data_path + "/" + str(i) + ".csv")
        print(data[["x", "y"]].values)
        splittedData.insert(i, data[["x", "y"]].values)

        # データの正規化(0~1)
        normalizedData.insert(i, TimeSeriesScalerMinMax().fit_transform(
            to_time_series_dataset([splittedData[i]])).flatten().reshape(-1, 2))

    return normalizedData