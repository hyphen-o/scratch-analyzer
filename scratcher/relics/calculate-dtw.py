import os
import pandas as pd
import numpy as np
from tslearn.preprocessing import TimeSeriesScalerMinMax
from tslearn.utils import to_time_series_dataset

from flask import Flask, make_response, request
from flask_cors import CORS

api = Flask(__name__)
CORS(api)

splittedData = []
prjIds = []
sprites = []
nomalizedData = []
x = []
y = []

def post():
    x.clear()
    y.clear()
    result = request.form["data"].lstrip("[").rstrip("]").split(",")
    resultLen = len(result)
    for i in range(resultLen):
        if (i < resultLen / 2):
            x.append(result[i])
        else:
            y.append(result[i])
    return make_response("post response")

@api.route("/get", methods=["GET"])
def get():
    result = calculateDtw(x, y)
    return result

# 検索データセットの読み込み
def loadDataset(splittedDataPath):
    print("loading dataset")

    fileLen = 0

    # 検索対象ファイルの数確認
    for pathName, dirName, fileNames in os.walk(splittedDataPath):
        fileLen = len(fileNames)
        for fileName in fileNames:
            if fileName.startswith("."):
                fileLen -= 1
    

    # 1動作のcsvを読み込み，配列に保持（配列のインデックス=動作番号）
    for i in range(fileLen):
        data = pd.read_csv(splittedDataPath + "/" + str(i) + ".csv")
        splittedData.insert(i, data[["x", "y"]].values)
        prjIds.insert(i, data["prjId"].values[0])
        sprites.insert(i, data["sprite"].values[0])
       
        # データの正規化(0~1)
        nomalizedData.insert(i, TimeSeriesScalerMinMax().fit_transform(to_time_series_dataset([splittedData[i]])).flatten().reshape(-1, 2))

    print("loaded dataset")
    

# 入力と各動作のDTW距離を算出
def calculateDtw(inputX, inputY):
    # 入力の整形
    inputData = []
    for i in range(len(inputX)):
        inputData.append(inputX[i])
        inputData.append(inputY[i])    
    inputData = np.array(inputData)
    inputData = inputData.reshape(len(inputX), 2)
    inputData = TimeSeriesScalerMinMax().fit_transform(to_time_series_dataset([inputData])).flatten().reshape(-1, 2)
       
    # 各動作ごとにDTW距離を算出
    dtwResults = pd.DataFrame(columns=["moveNum", "prjId", "sprite", "dtw"])   
    for i in range(len(splittedData)):
        dtwVal = dtw(inputData, nomalizedData[i])[1]
        addRow = pd.DataFrame([[str(i), str(prjIds[i]), sprites[i], dtwVal]], columns=["moveNum", "prjId", "sprite", "dtw"])
        dtwResults = dtwResults.append(addRow)

    dtwResults = dtwResults.sort_values("dtw") # このdtwResultsは，csv出力することでローカルに結果を保存可能
    return dtwResults.to_json(orient="records")

# DTW距離を算出
def dtw(x, y):
    # xのデータ数，yのデータ数をそれぞれTx,Tyに代入
    Tx = len(x)
    Ty = len(y)
    
    # C:各マスの累積コスト，　B：最小コストの行/列番号
    C = np.zeros((Tx, Ty))
    B = np.zeros((Tx, Ty, 2), int)
    
    # 一番初めのマスのコストを，xとyのそれぞれ一番初めの値にする
    C[0, 0] = dist(x[0], y[0])
    
    # 動的計画法を用いる
    # 左下のマスからスタートし，各マスに到達するため最小の累積コストを1マスずつ求める
    
    # 境界条件：両端が左下と右上にあること
    # 単調性：左下から始まり，右，上，右上のいずれかにしか進まないこと
    # 連続性：繋がっていること
    
    # 一番下の行は，真っ直ぐ右にコストが累積される
    for i in range(Tx):
        C[i, 0] = C[i - 1, 0] + dist(x[i], y[0])
        B[i, 0] = [i - 1, 0]
        
    # 同様に一番左の列は，真っ直ぐ上にコストが累積される
    for j in range(1, Ty):
        C[0, j] = C[0, j - 1] + dist(x[0], y[j])
        B[0, j] = [0, j - 1]
        
    # その他のマスの累積コストを求める
    for i in range(1, Tx):
        for j in range(1, Ty):
            pi, pj, m = get_min(C[i - 1, j],
                                C[i, j - 1],
                                C[i - 1, j - 1],
                                i, j)
            # get_minで返ってきた最小コストを累積コストに足す
            C[i, j] = dist(x[i], y[j]) + m
            # get_minで返ってきた最小コストの行/列番号を保持
            B[i, j] = [pi, pj]
    # 最終的な右上（最終の到達点）のコスト
    cost = C[-1, -1]
    
    path = [[Tx - 1, Ty - 1]]
    
    # 逆順にたどることでパスを求める
    i = Tx - 1
    j = Ty - 1
    
    while((B[i, j][0] != 0) or (B[i, j][1] != 0)):
        path.append(B[i, j])
        i, j = B[i, j].astype(int)
    path.append([0, 0])
    return np.array(path), cost, C

# 距離算出
def dist(a, b):
    return ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** 0.5

# 最小値算出
def get_min(m0, m1, m2, i, j):
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

loadDataset("./splitted")
api.run(host="0.0.0.0", port=49513, debug=True)