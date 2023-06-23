import sys

sys.path.append('../')

from utils import toFiles
from dtw import DTW


PROJECT_PATH = sys.path[-1] + "utils/coordinate_csv"  # ルートディレクトリからのパスを指定
RESULT_PATH = "../out_csv/result.csv"

# データの整形
normalizedData = dataset.loadCoordinate(PROJECT_PATH)

# DTWクラスのインスタンス生成
# 引数にウインドウサイズを指定すると部分一致DTWを計算
dtw = DTW()

# データセットの読み込み
dtw.setData(normalizedData)
# DTW距離の計算
result = dtw.getDtw()
toFiles.dfToFile(result, RESULT_PATH)

print(result)
