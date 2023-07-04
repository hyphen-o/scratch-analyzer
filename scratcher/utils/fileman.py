import numpy as np
import pandas as pd
import os
import csv
import json

def count_files(dir_path):
    file_count = 0

    # ディレクトリ内のファイルとディレクトリのリストを取得
    items = os.listdir(dir_path)

    for item in items:
        item_path = os.path.join(dir_path, item)
        if os.path.isfile(item_path):  # ファイルであればカウント
            file_count += 1

    return file_count

def remove_extension(file_name):
    base_name = os.path.splitext(file_name)[0]
    return base_name


def numpy_to_tile(data, path):
    np.savetxt(path, data, delimiter=',')
    print('save numpyFile')


def df_to_file(data, path):
    df = pd.DataFrame(data)
    df.to_csv(path, sep=',', index=False)
    print('save dataframeFile')

def json_to_file(data, path):
    with open(path, "w") as json_file:
        json.dump(data, json_file)

def read_json_file(path):
    try:
        with open(path, 'r') as file:
            json_data = json.load(file)
            return json_data
    except Exception as e:
        print('JSON読み込み中にエラーが発生しました．')
        print(e)
        

class ToCsv:
    def __init__(self, csv_path, rowNames):
        self.__CSV_PATH = csv_path
        with open(self.__CSV_PATH, 'w') as f:
            writer = csv.writer(f)
            writer.writerow(rowNames)
    
    def writeRow(self, rowData):
        with open(self.__CSV_PATH, 'a') as f:
            writer = csv.writer(f)
            writer.writerow(rowData)
