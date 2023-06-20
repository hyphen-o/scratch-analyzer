import csv
import math
import pandas as pd
import sys
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


def writeToCsv(key, x, y, wait, csv_name):
    with open(f'coordinate_csv/{csv_name}', 'a') as f:
        writer = csv.writer(f)
        writer.writerow([key, x, y, wait])


def getStepMovement(degrees, steps):
    degree_rad = math.radians(90 - degrees)
    dx = steps * math.cos(degree_rad)
    dy = steps * math.sin(degree_rad)
    return (dx, dy)


def calculate(index, df_length, x, y, degree, block_info, csv_name):
    wait = 0.0
    for i in range(index, df_length):
        try:
            if (block_info.iloc[i][0] == 'Nextscript'):
                return (degree, x, y)
            if (not pd.isna(block_info.iloc[i][2])):
                dic = ast.literal_eval(block_info.iloc[i][2])
                for key in dic.keys():
                    if key in MOVE:
                        if key == 'DX':
                            x = float(x) + float(dic[key][1][1])
                        elif key == 'DY':
                            y = float(y) + float(dic[key][1][1])
                    elif key in SET:
                        if key == 'X':
                            x = float(dic[key][1][1])
                        elif key == 'Y':
                            y = float(dic[key][1][1])
                    elif key in DEGREE:
                        if key == 'DEGREES':
                            if (block_info.iloc[i][0] == 'motion_turnleft'):
                                print('turnleft')
                                degree = float(degree) + float(dic[key][1][1])
                            elif (block_info.iloc[i][0] == 'motion_turnright'):
                                print('turnright')
                                degree = float(degree) - float(dic[key][1][1])
                        if key == 'DIRECTION':
                            degree = float(dic[key][1][1])
                    elif key == 'STEPS':
                        result = getStepMovement(
                            float(degree), float(dic[key][1][1]))
                        print(result[0])
                        print(result[1])
                        x = float(x) + result[0]
                        y = float(y) + result[1]
                    elif key in WAIT:
                        wait += float(dic[key][1][1])
            if (not pd.isna(block_info.iloc[i][1])):
                print('write')
                writeToCsv(None, x, y, wait, csv_name)
                writeToCsv(block_info.iloc[i][1], None, None, None, csv_name)
                wait = 0.0
        except Exception as e:
            print(e)

    return (degree, x, y)


def getMovement(block_info, csv_name):
    degree = block_info.iloc[0][0]
    x = block_info.iloc[0][1]
    y = block_info.iloc[0][2]
    df_length = len(block_info.index)
    print(x)
    print(y)
    print(degree)

    try:
        for i in range(df_length):
            block_name = block_info.iloc[i][0]
            if (block_name == 'event_whenflagclicked'):
                result = calculate(i, df_length, x, y,
                                   degree, block_info, csv_name)
                degree = result[0]
                x = result[1]
                y = result[2]
                break
        for i in range(df_length):
            block_name = block_info.iloc[i][0]
            if ('event' in block_name):
                if (block_name != 'event_whenflagclicked'):
                    result = calculate(i, df_length, x, y,
                                       degree, block_info, csv_name)
                    degree = result[0]
                    x = result[1]
                    y = result[2]

    except Exception as e:
        print('error: ' + str(e))


j = 0
for filename in os.listdir("./sorted_csv"):
    j += 1
    try:
        print(j)
        blocks = []
        flg = False
        sorted_csv = pd.read_csv(f'sorted_csv/{filename}')
        for i in range(1, len(sorted_csv.index)):
            if ('event' in sorted_csv.iloc[i][0]):
                if (sorted_csv.iloc[i][0] in blocks):
                    flg = True
                else:
                    blocks.append(sorted_csv.iloc[i][0])
            print(i)
        if (flg):
            continue
        filename = re.sub(r"\D", "", filename)
        csv_name = f'{filename}_coordinate.csv'
        if (os.path.exists(f'coordinate_csv/{csv_name}')):
            print('exist')
            continue
        if (len(sorted_csv.index) > 1):
            with open(f'coordinate_csv/{csv_name}', 'w') as f:
                writer = csv.writer(f)
                writer.writerow(['key', 'x', 'y', 'wait'])
            getMovement(sorted_csv, csv_name)
            coordinate_csv = pd.read_csv(f'coordinate_csv/{csv_name}')
            if (not len(coordinate_csv.index)):
                os.remove(f'coordinate_csv/{csv_name}')
    except Exception as e:
        print(e)
