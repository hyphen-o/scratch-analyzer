import sys
sys.path.append('../')

from utils import DfManager

import csv
import math
import pandas as pd
import ast
import os
import re

# 座標情報を格納しているキー名
MOVE = ['DX', 'DY']
SET = ['X', 'Y']
DEGREE = ['DEGREES', 'DIRECTION']
STEP = ['STEPS']
BOUND = ['motion_ifonedgebounce']
# 待機時間情報を格納しているキー名
WAIT = ['DURATION', 'SECS']


class Tracker:
    # 座標情報を格納しているキー名
    __MOVE = ['DX', 'DY']
    __SET = ['X', 'Y']
    __DEGREE = ['DEGREES', 'DIRECTION']
    __STEP = ['STEPS']
    __BOUND = ['motion_ifonedgebounce']
    # 待機時間情報を格納しているキー名
    __WAIT = ['DURATION', 'SECS']


    def __init__(self, project):
        if isinstance(project, str):
            self.__sorted_df = pd.read_csv(project)
        elif isinstance(project, pd.DataFrame):
            self.__sorted_df = project
        else:
            print("プロジェクトへのパスか，プロジェクトを入力としてください．")
            return

        self.__df = DfManager(['key', 'x', 'y', 'wait', 'move_index'])
        
    
    def to_csv(self, dir_path):
        self.__df.to_csv(dir_path)
    
    def __get_step_movement(degrees, steps):
        degree_rad = math.radians(90 - degrees)
        dx = steps * math.cos(degree_rad)
        dy = steps * math.sin(degree_rad)
        return (dx, dy)
    
    def get_coordinate(self):
        self.__degree = self.__sorted_df.iloc[0][0]
        self.__x = self.__sorted_df.iloc[0][1]
        self.__y = self.__sorted_df.iloc[0][2]
        self.__df_length = len(self.__sorted_df.index)

        try:
            for i in range(self.__df_length):
                block_name = self.__sorted_df.iloc[i][0]
                if (block_name == 'event_whenflagclicked'):
                    calculate_coordinate(i)
                    break
            for i in range(self.__df_length):
                block_name = self.__sorted_df.iloc[i][0]
                if ('event' in block_name):
                    if (block_name != 'event_whenflagclicked'):
                        calculate_coordinate(i)

        except Exception as e:
            print('error: ' + str(e))

        def calculate_coordinate(index):
            wait = 0.0
            for i in range(index, self.__df_length):
                try:
                    if (self.__sorted_df.iloc[i][0] == 'SCRIPT'):
                        return
                    if (not pd.isna(self.__sorted_df.iloc[i][2])):
                        dic = ast.literal_eval(self.__sorted_df.iloc[i][2])
                        for key in dic.keys():
                            if key in MOVE:
                                if key == 'DX':
                                    self.__x = float(self.__x) + float(dic[key][1][1])
                                elif key == 'DY':
                                    self.__y = float(self.__y) + float(dic[key][1][1])
                            elif key in SET:
                                if key == 'X':
                                    self.__x = float(dic[key][1][1])
                                elif key == 'Y':
                                    self.__y = float(dic[key][1][1])
                            elif key in DEGREE:
                                if key == 'DEGREES':
                                    if (self.__sorted_df.iloc[i][0] == 'motion_turnleft'):
                                        print('turnleft')
                                        self.__degree = float(self.__degree) + float(dic[key][1][1])
                                    elif (self.__sorted_df.iloc[i][0] == 'motion_turnright'):
                                        print('turnright')
                                        self.__degree = float(self.__degree) - float(dic[key][1][1])
                                if key == 'DIRECTION':
                                    self.__degree = float(dic[key][1][1])
                            elif key == 'STEPS':
                                result = self.__get_step_movement(
                                    float(self.__degree), float(dic[key][1][1]))
                                self.__x = float(self.__x) + result[0]
                                self.__y = float(self.__y) + result[1]
                            elif key in WAIT:
                                wait += float(dic[key][1][1])
                        self.__df.add_row([None, self.__x, self.__y, wait, i])
                        wait = 0.0
                except Exception as e:
                    print(e)

            return
    

j = 0

# for filename in os.listdir("../sorted_csv"):
#     try:
#         print(j)
#         if j > 2000:
#             break
#         coordinated_csv = pd.read_csv(f'../sorted_csv/{filename}')
#         filename = re.sub(r"\D", "", filename)
#         csv_name = f'{filename}.csv'
#         if (os.path.exists(f'../coordinate_csv2/{csv_name}')):
#             print('exist')
#             continue
#         if (coordinated_csv.shape[0] > 3):
#             print(coordinated_csv.shape[0])
#             with open(f'../coordinate_csv2/{csv_name}', 'w') as f:
#                 writer = csv.writer(f)
#                 writer.writerow(['key', 'x', 'y', 'wait', 'move_index', filename])
#             getMovement(coordinated_csv, csv_name)
#             coordinate_csv = pd.read_csv(f'../coordinate_csv2/{csv_name}')
#             if (not len(coordinate_csv.index)):
#                 os.remove(f'../coordinate_csv2/{csv_name}')
#             j += 1
#     except Exception as e:
#         print(e)
