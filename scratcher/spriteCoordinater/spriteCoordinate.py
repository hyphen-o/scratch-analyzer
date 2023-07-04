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


def writeToCsv(key, x, y, wait, csv_name):
    with open(f'../coordinate_csv2/{csv_name}', 'a') as f:
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
                        x = float(x) + result[0]
                        y = float(y) + result[1]
                    elif key in WAIT:
                        wait += float(dic[key][1][1])
                writeToCsv(None, x, y, wait, csv_name)
                wait = 0.0
        except Exception as e:
            print(e)

    return (degree, x, y)


def getMovement(block_info, csv_name):
    degree = block_info.iloc[0][0]
    x = block_info.iloc[0][1]
    y = block_info.iloc[0][2]
    df_length = len(block_info.index)

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
for filename in os.listdir("../sorted_csv"):
    try:
        print(j)
        if j > 2000:
            break
        coordinated_csv = pd.read_csv(f'../sorted_csv/{filename}')
        filename = re.sub(r"\D", "", filename)
        csv_name = f'{filename}.csv'
        if (os.path.exists(f'../coordinate_csv2/{csv_name}')):
            print('exist')
            continue
        if (coordinated_csv.shape[0] > 3):
            print(coordinated_csv.shape[0])
            with open(f'../coordinate_csv2/{csv_name}', 'w') as f:
                writer = csv.writer(f)
                writer.writerow(['key', 'x', 'y', 'wait', filename])
            getMovement(coordinated_csv, csv_name)
            coordinate_csv = pd.read_csv(f'../coordinate_csv2/{csv_name}')
            if (not len(coordinate_csv.index)):
                os.remove(f'../coordinate_csv2/{csv_name}')
            j += 1
    except Exception as e:
        print(e)
