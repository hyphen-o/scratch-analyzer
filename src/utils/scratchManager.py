import sys
sys.path.append('../')

import csv
from utils import ToCSV, jsonToFile
from api import scratchApi

class scratchManager:
    def __init__(self, id):
        self.__ID = id
        self.__project = scratchApi.get_project(self.__ID)
        self.__sprite = self.__project['targets'][1]
        self.__blocks = self.__getAllblocks()
    
    def getProject(self):
        return self.__project
    
    def getBlocks(self):
        return self.__blocks
    
    def toJson(self, dir_path=".", type="project"):
        #typeに応じて出力するJSONファイルを変える
        match(type):
            case "project":
                jsonToFile(self.__project, f'{dir_path}/{self.__ID}.json')
            case "sprite":
                jsonToFile(self.__sprite, f'{dir_path}/{self.__ID}_sprite.json')
            case "blocks":
                jsonToFile(self.__blocks, f'{dir_path}/{self.__ID}_blocks.json')

    def getBlocksLength(self):
        return len(self.__blocks)
    
    def isDataset(self, ava_path):

        ava_blocks = []
        #フィルタリング用CSVの読み込み
        with open(ava_path, encoding = 'utf-8-sig') as f:
            reader = csv.reader(f)
            for row in reader:
                ava_blocks.append(row)
        
        isDataset = self.__filterJson(ava_blocks)
        return isDataset
 
    def sortBlocks(self, dir_path):
        self.__CSV_PATH = f'{dir_path}/{self.__ID}_sorted.csv'
        toCsv = ToCSV(self.__CSV_PATH, ['BlockName', 'Key', 'Field'])
        #スプライトの初期座標，角度をはじめに書き込む
        toCsv.writeRow(self.__sprite['direction'], self.__sprite['x'], self.__sprite['y'])


    # Private関数

    def __getAllblocks(self):
        return self.__project['targets'][1]['blocks']

    #フィルタリング
    def __filterJson(self, ava_blocks):
        for k in self.__blocks:
            for block, ava in ava_blocks:
                if self.__blocks[k]['opcode'] == block and int(ava) == 0: 
                    return False
        return True
    