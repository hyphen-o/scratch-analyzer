import numpy as np
import pandas as pd
import csv
import json


def numpyToFile(data, path):
    np.savetxt(path, data, delimiter=',')
    print('save numpyFile')


def dfToFile(data, path):
    df = pd.DataFrame(data)
    df.to_csv(path, sep=',', index=False)
    print('save dataframeFile')

def jsonToFile(data, path):
    with open(path, "w") as json_file:
        json.dump(data, json_file)

class ToCSV:
    def __init__(self, csv_path, rowNames):
        self.__CSV_PATH = csv_path
        with open(self.__CSV_PATH, 'w') as f:
            writer = csv.writer(f)
            writer.writerow(rowNames)
    
    def writeRow(self, rowData):
        with open(self.__CSV_PATH, 'a') as f:
            writer = csv.writer(f)
            writer.writerow(rowData)
