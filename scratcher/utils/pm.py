import sys
sys.path.append('../')

import csv
from utils import ToCSV, jsonToFile, readJsonFile
from api import scratchApi

class projectManager:
    # 座標情報を格納しているキー名
    __MOVE = ['STEPS', 'DEGREES', 'DIRECTION', 'X', 'Y', 'DX', 'DY']
    # 待機時間情報を格納しているキー名
    __WAIT = ['DURATION', 'SECS']

    def __init__(self, id):
        self.__ID = id
        self.__project = scratchApi.get_project(self.__ID)
        self.__sprite = self.__project['targets'][1]
        self.__blocks = self.__project['targets'][1]['blocks']
    
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
 
    def sortBlocks(self, dir_path, file_name=None):
        if(file_name):
            self.__CSV_PATH = f'{dir_path}/{file_name}'
        else:
            self.__CSV_PATH = f'{dir_path}/{self.__ID}_sorted.csv'
        
        self.__toCSV = ToCSV(self.__CSV_PATH, ['BlockName', 'Key', 'Field'])
        #スプライトの初期座標，角度をはじめに書き込む
        self.__toCSV.writeRow([self.__sprite['direction'], self.__sprite['x'], self.__sprite['y']])

        for block_hash, v in self.__blocks.items():
            if ('event' in v['opcode']):
                self.__writeEventBlock(block_hash)


    # Private関数

    #フィルタリング
    def __filterJson(self, ava_blocks):
        for k in self.__blocks:
            for block, ava in ava_blocks:
                if self.__blocks[k]['opcode'] == block and int(ava) == 0: 
                    return False
        return True
    
    def __identifyBlocks(self, block_hash):
        try:
            if (self.__blocks[block_hash]['inputs'] != None):
                    for key in self.__blocks[block_hash]['inputs']:
                        # 制御ブロックor条件付きブロックの場合その中身も見る
                        if (key == 'SUBSTACK' or key == 'CONDITION'):
                            self.__writeBlocks(self.__blocks[block_hash]['inputs'][str(key)][1])
                        # 条件ブロックの中身を見る
                        if (key == 'KEY_OPTION' and self.__blocks[block_hash]['inputs']['KEY_OPTION'][1] != None):
                            self.__writeBlocks(self.__blocks[block_hash]['inputs'][str(key)][1], key)
            # 次のブロックを見る
            if (self.__blocks[block_hash]['next'] != None):
                self.__writeBlocks(self.__blocks[block_hash]['next'])
        except Exception as e:
            print('1')
            print(e)
    
    def __writeBlocks(self, block_hash, field_name = None):
        try:
            block_name = self.__blocks[block_hash]['opcode']

            flg = False
            if(field_name):
                self.__toCSV.writeRow([block_name, self.__blocks[block_hash]['fields'][field_name][0], None])
            else:
                if (self.__blocks[block_hash]['inputs'] == "{{}}"):
                    self.__toCSV.writeRow([block_name, None, None])
                else:
                    for key in self.__blocks[block_hash]['inputs']:
                        if (key in self.__MOVE or key in self.__WAIT):
                            self.__toCSV.writeRow([block_name, None, self.__blocks[block_hash]['inputs']])
                            flg = True
                            break
                    if not flg:
                        self.__toCSV.writeRow([block_name, None, None])

            self.__identifyBlocks(block_hash)
        except Exception as e:
            print('2')
            print(e)
    
    def __writeEventBlock(self, block_hash):
    # 次のブロックがあるか確認
        try:
            if (self.__blocks[block_hash]['next'] != None):
                block_name = self.__blocks[block_hash]['opcode']
                # CSVファイルにブロック情報を書き込む
                self.__toCSV.writeRow(['Nextscript', None, None])
                if (block_name == 'event_whenkeypressed'):
                    key_name = self.__blocks[block_hash]['fields']['KEY_OPTION'][0]
                    self.__toCSV.writeRow([block_name, key_name, None])
                else:
                    self.__toCSV.writeRow([block_name, None, None])
                
                self.__writeBlocks(self.__blocks[block_hash]['next'])
        except Exception as e:
            print('3')
            print(e)
    