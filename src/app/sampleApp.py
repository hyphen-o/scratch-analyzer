import sys

sys.path.append('../')

from utils import manageFiles, dataset
from dtw import DTW


PROJECT_PATH = sys.path[-1] + "splitted/splitted-a"  # ルートディレクトリからのパスを指定
RESULT_PATH = "../out_csv/result-a.csv"

# データの整形
normalizedData = dataset.loadCoordinate(PROJECT_PATH)
print(normalizedData)

# DTWクラスのインスタンス生成
# 引数にウインドウサイズを指定すると部分一致DTWを計算
dtw = DTW()

# データセットの読み込み
dtw.setData(normalizedData)
# DTW距離の計算
result = dtw.getDtw()
manageFiles.dfToFile(result, RESULT_PATH)

print(result)
