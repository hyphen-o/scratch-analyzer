import sys
sys.path.append('../')

import csv
from utils import json_to_file
from api import scratch_client
from tools import Sorter, Tracker

class ProjectManager:
    # 座標情報を格納しているキー名
    __MOVE = ['STEPS', 'DEGREES', 'DIRECTION', 'X', 'Y', 'DX', 'DY']
    # 待機時間情報を格納しているキー名
    __WAIT = ['DURATION', 'SECS']

    def __init__(self, id):
        try:
            self.__ID = id
            self.__project = scratch_client.get_project(self.__ID)
            self.__sprite = self.__project['targets'][1]
            self.__blocks = self.__project['targets'][1]['blocks']
        except Exception as e:
            print('Scratch3.0以降の作品を入力してください．')
            print(e)
    
    def get_id(self):
        return self.__ID
    
    def get_project(self):
        return self.__project
    
    def get_blocks(self):
        return self.__blocks
    

    def get_blocks_length(self):
        return len(self.__blocks)
    
    def get_sorted_blocks(self, dir_path=None):
        sorter = Sorter(self.__project)
        if(dir_path):
            sorter.sort_blocks()
            sorter.to_csv(dir_path)
            return
        else:
            return sorter.sort_blocks()
        
    def get_coordinate(self, dir_path=None):
        tracker = Tracker(self.get_sorted_blocks())
        if(dir_path):
            tracker.get_coordinate()
            tracker.to_csv(dir_path)
            return
        else:
            return tracker.get_coordinate()
        
    def to_json(self, dir_path=".", type="project"):
        #typeに応じて出力するJSONファイルを変える
        match(type):
            case "project":
                json_to_file(self.__project, f'{dir_path}/{self.__ID}.json')
            case "sprite":
                json_to_file(self.__sprite, f'{dir_path}/{self.__ID}_sprite.json')
            case "blocks":
                json_to_file(self.__blocks, f'{dir_path}/{self.__ID}_blocks.json')
                
    def is_dataset(self, ava_path="utils/filter/filter.csv"):

        ava_blocks = []
        #フィルタリング用CSVの読み込み
        with open(ava_path, encoding = 'utf-8-sig') as f:
            reader = csv.reader(f)
            for row in reader:
                ava_blocks.append(row)
        
        isDataset = self.__filter_json(ava_blocks)
        return isDataset
    


    # Private関数

    #フィルタリング
    def __filter_json(self, ava_blocks):
        for k in self.__blocks:
            for block, ava in ava_blocks:
                if self.__blocks[k]['opcode'] == block and int(ava) == 0: 
                    return False
        return True
    
    