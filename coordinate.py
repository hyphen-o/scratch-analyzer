import os
import time
import sys
import json
import requests
import csv
import math
import pandas as pd
import ast
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome import service as fs
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from concurrent.futures import ThreadPoolExecutor

# 座標情報を格納しているキー名
MOVE = ['DX', 'DY']
SET = ['X', 'Y']
DEGREE = ['DEGREES', 'DIRECTION']
STEP = ['STEPS']
BOUND = ['motion_ifonedgebounce']
# 待機時間情報を格納しているキー名
WAIT = ['DURATION', 'SECS']

# キー名と一致するセレニウムキーオプションの辞書
KEY_DICT = {'space': Keys.SPACE,
            'up arrow': Keys.ARROW_UP,
            'down arrow': Keys.ARROW_DOWN,
            'right arrow': Keys.ARROW_RIGHT,
            'left arrow': Keys.ARROW_LEFT,
            'any': Keys.SPACE}

# 作品のASTを取得する
id = "747365086"

block_info = pd.read_csv(f'out_csv/{id}_sorted.csv')


csv_name = f'{id}_coordinate.csv'
with open(f'coordinate_csv/{csv_name}', 'w') as f:
    writer = csv.writer(f)
    writer.writerow(['key', 'x', 'y', 'wait'])


def writeToCsv(key, x, y, wait):
    with open(f'coordinate_csv/{csv_name}', 'a') as f:
        writer = csv.writer(f)
        writer.writerow([key, x, y, wait])


def getStepMovement(degrees, steps):
    degree_rad = math.radians(90 - degrees)
    dx = steps * math.cos(degree_rad)
    dy = steps * math.sin(degree_rad)
    return (dx, dy)


def calculate(index, df_length, x, y, degree):
    wait = 0
    for i in range(index, df_length):
        if (block_info.iloc[i][0] == 'Nextscript'):
            return (degree, x, y)
        if (not pd.isna(block_info.iloc[i][2])):
            dic = ast.literal_eval(block_info.iloc[i][2])
            for key in dic.keys():
                if key in MOVE:
                    if key == 'DX':
                        x = x + int(dic[key][1][1])
                    elif key == 'DY':
                        y = y + int(dic[key][1][1])
                    print('progX: ' + str(x))
                    print('progY: ' + str(y))
                elif key in SET:
                    if key == 'X':
                        x = int(dic[key][1][1])
                    elif key == 'Y':
                        y = int(dic[key][1][1])
                    print('progX: ' + str(x))
                    print('progY: ' + str(y))
                elif key in DEGREE:
                    if key == 'DEGREES':
                        if (block_info.iloc[i][0] == 'motion_turnleft'):
                            print('turnleft')
                            degree = degree + int(dic[key][1][1])
                        elif (block_info.iloc[i][0] == 'motion_turnright'):
                            print('turnright')
                            degree = degree - int(dic[key][1][1])
                    if key == 'DIRECTION':
                        degree = int(dic[key][1][1])
                    print('progdegeree' + str(degree))
                elif key == 'STEPS':
                    result = getStepMovement(
                        degree, int(dic[key][1][1]))
                    print(result[0])
                    print(result[1])
                    x = x + result[0]
                    y = y + result[1]
                elif key in WAIT:
                    wait += int(dic[key][1][1])
        if (not pd.isna(block_info.iloc[i][1])):
            print('write')
            writeToCsv(None, x, y, wait)
            writeToCsv(block_info.iloc[i][1], None, None, None)
            wait = 0

    return (degree, x, y)


def getMovement():
    degree = block_info.iloc[0][0]
    x = block_info.iloc[0][1]
    y = block_info.iloc[0][2]
    df_length = len(block_info.index)

    try:
        for i in range(df_length):
            block_name = block_info.iloc[i][0]
            if (block_name == 'event_whenflagclicked'):
                result = calculate(i, df_length, x, y, degree)
                degree = result[0]
                x = result[1]
                y = result[2]
                break
        for i in range(df_length):
            block_name = block_info.iloc[i][0]
            if ('event' in block_name):
                if (block_name != 'event_whenflagclicked'):
                    result = calculate(i, df_length, x, y, degree)
                    degree = result[0]
                    x = result[1]
                    y = result[2]

    except Exception as e:
        print('error: ' + str(e))

    # try:
    #     print('Movement change-------')
    #     for i in range(df_length):
    #         if (not pd.isna(df_none.iloc[i][2])):
    #             dic = ast.literal_eval(df_none.iloc[i][2])
    #             for key in dic.keys():
    #                 if key in MOVE:
    #                     if key == 'DX':
    #                         program_x = program_x + int(dic[key][1][1])
    #                     elif key == 'DY':
    #                         program_y = program_y + int(dic[key][1][1])
    #                     print('progX: ' + str(program_x))
    #                     print('progY: ' + str(program_y))
    #                 elif key in SET:
    #                     if key == 'X':
    #                         program_x = int(dic[key][1][1])
    #                     elif key == 'Y':
    #                         program_y = int(dic[key][1][1])
    #                     print('progX: ' + str(program_x))
    #                     print('progY: ' + str(program_y))
    #                 elif key in DEGREE:
    #                     program_degrees = int(dic[key][1][1])
    #                 elif key == 'STEPS':
    #                     result = getStepMovement(
    #                         program_degrees, int(dic[key][1][1]))
    #                     print(result[0])
    #                     print(result[1])
    #                     program_x = program_x + result[0]
    #                     program_y = program_y + result[1]
    #         if (not pd.isna(df_none.iloc[i][1])):
    #             program_move.append([program_x, program_y])
    #             print(program_move)
    #             input_keys.append(df_none.iloc[i][1])
    #             print(input_keys)
    #     print('-------')
    # except Exception as e:
    #     print(e)


getMovement()
