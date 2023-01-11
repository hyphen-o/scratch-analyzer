import os
import time
import sys
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

# ids = pd.read_csv("/Users/socsel/dataset.csv", usecols=["p_ID"], dtype="str")
# retryIds = pd.read_csv("/Users/socsel/retryIds.csv", usecols=["p_ID"], dtype="str")
retryIds = pd.read_csv("out_csv/retryIds.csv",
                       usecols=["p_ID"], dtype="str")
retryIds = list(retryIds)

program_x = 0
program_y = 0
program_degrees = 60
input_flg = False
input_key = ''
index = 0

# 座標情報を格納しているキー名
MOVE = ['DX', 'DY']
SET = ['X', 'Y']
DEGREE = ['DEGREES']
STEP = ['STEPS']
BOUND = ['motion_ifonedgebounce']
# 待機時間情報を格納しているキー名
WAIT = ['DURATION', 'SECS']
# キー用の辞書
KEY_DICT = {'space': Keys.SPACE,
            'up arrow': Keys.ARROW_UP,
            'down arrow': Keys.ARROW_DOWN,
            'right arrow': Keys.ARROW_RIGHT,
            'left arrow': Keys.ARROW_LEFT,
            'any': Keys.SPACE}


# 作品のASTを取得する
id = "747365086"

df_none = pd.read_csv('out_csv/SortedScripts[3].csv')

chrome_service = fs.Service("/usr/local/bin/chromedriver")
driver = webdriver.Chrome(service=chrome_service)

driver.get("https://scratch.mit.edu/projects/" + str(id) + "/editor")

wait = WebDriverWait(driver, 15)
loadClassName = "loader_bottom-block_1-3rO"


def getStepMovement(degrees, steps):
    degree_rad = math.radians(90 - degrees)
    dx = steps * math.cos(degree_rad)
    dy = steps * math.sin(degree_rad)
    return dx, dy


def getMovement(index):
    global program_x
    global program_y
    global program_degrees
    global input_flg
    global input_key
    X = 0
    try:
        print('Movement change-------')
        for i in range(index, len(df_none.index)):
            print(index)
            if (not pd.isna(df_none.iloc[i][2])):
                dic = ast.literal_eval(df_none.iloc[i][2])
                for key in dic.keys():
                    if key in MOVE:
                        if key == 'DX':
                            program_x = program_x + int(dic[key][1][1])
                        elif key == 'DY':
                            program_y = program_y + int(dic[key][1][1])
                        print('progX: ' + str(program_x))
                        print('progY: ' + str(program_y))
                    elif key in SET:
                        if key == 'X':
                            program_x = int(dic[key][1][1])
                        elif key == 'Y':
                            program_y = int(dic[key][1][1])
                        print('progX: ' + str(program_x))
                        print('progY: ' + str(program_y))
                    elif key in DEGREE:
                        program_degrees = int(dic[key][1][1])
                    elif key == 'STEPS':
                        result = getStepMovement(
                            program_degrees, int(dic[key][1][1]))
                        print(result[0])
                        print(result[1])
                        program_x = program_x + result[0]
                        program_y = program_y + result[1]
            if (not pd.isna(df_none.iloc[i][1])):
                input_key = df_none.iloc[i][1]
                index = i + 1
                break
        print('-------')
        return index, input_key
    except Exception as e:
        print(e)


try:
    wait.until(EC.presence_of_element_located(
        (By.CLASS_NAME, loadClassName)))  # 作品のロード開始を待機
    wait.until_not(EC.presence_of_element_located(
        (By.CLASS_NAME, loadClassName)))  # 作品のロード完了を待機
except TimeoutException as te:
    print(str(id) + ": timeout")  # 作品が存在していないため，スキップ
    driver.close()
    sys.exit()

try:
    # スプライトのX座標,Y座標を取ってくる
    positionX = driver.find_elements(
        By.XPATH, '/html/body/div[1]/div/div[3]/div/div[2]/div[2]/div/div[1]/div[1]/div[1]/div[2]/label/input')
    for i in positionX:
        print(i.get_attribute("value"))
    positionY = driver.find_elements(
        By.XPATH, '/html/body/div[1]/div/div[3]/div/div[2]/div[2]/div/div[1]/div[1]/div[1]/div[3]/label/input')
    for i in positionY:
        print(i.get_attribute("value"))

    program_x = 0
    program_y = 0
    program_degrees = 30
    input_flg = False
    index = 0

    result = getMovement(index)
    input_flg = True
    index = result[0]
    print(index)
    input_key = result[1]

    start = driver.find_elements(
        By.CLASS_NAME, "green-flag_green-flag_1kiAo")

    start[0].click()
    print('click')

except Exception as e:
    print(str(id) + ": crash error")  # Scratchがクラッシュするエラー
    print(str(e))
    retryIds.append(str(id))  # エラーが発生した場合，後ほど再試行するためidを配列に追加して保持
    driver.close()
    sys.exit()

savePath = "/Users/keigo-o/Desktop/screenshots/" + str(id)
if not os.path.isdir(savePath):
    os.mkdir(savePath)

startTime = time.time()

# スクリーンショットを行う関数


def ScreenShot():
    for i in range(100):
        time.sleep(0.2)

        try:
            end = driver.find_elements(
                By.CSS_SELECTOR, ".green-flag_green-flag_1kiAo.green-flag_is-active_2oExT")
            if len(end) == 0:
                break  # 作品のプログラムが終了していれば，スクリーンショット収集終了
            png = driver.find_element(
                By.CLASS_NAME, "stage-wrapper_stage-canvas-wrapper_3ewmd").screenshot_as_png  # スクリーンショットを取得
        except Exception as e:
            print(str(id) + ": error")  # 予期せぬエラー
            print(e)
            retryIds.append(str(id))  # エラーが発生した場合，後ほど再試行するためidを配列に追加して保持
            driver.close()
            break

        try:
            with open(savePath + "/" + str(id) + "-" + str(i) + ".png", "wb") as f:
                f.write(png)
            print("save png: " + str(i))
        except OSError as oe:
            print("save error")  # 画像保存失敗エラー
            driver.close()
            continue
    driver.close()

# 自動入力を行う関数


def AutoInput():
    global program_x
    global program_y
    global program_degrees
    global input_flg
    global input_key
    global index
    for i in range(10000000):

        try:
            end = driver.find_elements(
                By.CSS_SELECTOR, ".green-flag_green-flag_1kiAo.green-flag_is-active_2oExT")
            if len(end) == 0:
                break  # 作品のプログラムが終了していれば，スクリーンショット収集終了

            if not input_flg:
                result = getMovement(index)
                input_flg = True
                index = result[0]
                print(index)
                input_key = result[1]

            # スプライトのX座標Y座標を取得
            for j in positionX:
                X = j.get_attribute("value")
            for j in positionY:
                Y = j.get_attribute("value")

            print('progX: ' + str(round(program_x)))
            print('progY: ' + str(round(program_y)))
            print('X: ' + str(X))
            print('Y: ' + str(Y))

            if (input_key and abs(round(program_x) - int(X)) < 5 and abs(round(program_y) - int(Y)) < 5):
                actions = ActionChains(driver)
                print('input!!!!!!!!!!')
                input_flg = False
                print(input_key)
                actions.key_down(KEY_DICT[input_key]).perform()
                time.sleep(0.0005)
                actions.key_up(KEY_DICT[input_key]).perform()
                # actions.send_keys(KEY_DICT[input_key]).perform()
                input_key = ''

        except Exception as e:
            print(str(id) + ": error")  # 予期せぬエラー
            print(e)
            driver.close()
            break


with ThreadPoolExecutor(max_workers=2) as executor:
    executor.submit(ScreenShot)
    executor.submit(AutoInput)

elapsedTime = time.time() - startTime
print(str(id) + ": " + str(elapsedTime) + "s")

df = pd.DataFrame(retryIds, columns=["p_ID"])

if len(retryIds) > 1:
    df.to_csv("retryIds.csv")

driver.close()
driver.quit()
