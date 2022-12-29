import os
import time
import sys
import math
import subprocess
import pandas as pd
import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome import service as fs
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from concurrent.futures import ThreadPoolExecutor

# ids = pd.read_csv("/Users/socsel/dataset.csv", usecols=["p_ID"], dtype="str")
# retryIds = pd.read_csv("/Users/socsel/retryIds.csv", usecols=["p_ID"], dtype="str")
retryIds = pd.read_csv("out_csv/retryIds.csv",
                       usecols=["p_ID"], dtype="str")
retryIds = list(retryIds)

# 座標情報を格納しているキー名
MOVE = ['DX', 'DY']
SET = ['X', 'Y']
DEGREE = ['DEGREES']
STEP = ['STEPS']
# 待機時間情報を格納しているキー名
WAIT = ['DURATION', 'SECS']


# 作品のASTを取得する
id = "747365086"

program_x = 0
program_y = 0

df_none = pd.read_csv('out_csv/SortedScripts[0].csv')
for i in range(len(df_none.index)):
    print(df_none.iloc[i][1])
    print(df_none.iloc[i][2])


chrome_service = fs.Service("/usr/local/bin/chromedriver")
driver = webdriver.Chrome(service=chrome_service)

driver.get("https://scratch.mit.edu/projects/" + str(id) + "/editor")

wait = WebDriverWait(driver, 15)
loadClassName = "loader_bottom-block_1-3rO"

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


def getMovement(index):
    X = 0
    if (not pd.isna(df_none.iloc[index][2])):
        print(df_none.iloc[index][2] + '!!!!!!!!!!!!!!!!!!!')
        # json_data = json.loads(str(df_none.iloc[index][2]))
        # for k, v in json_data.items():
        #     print(k + '!!!!!')
        #     print(v)

    if (not pd.isna(df_none.iloc[index][1])):
        return df_none.iloc[index][1]

    if (index < len(df_none.index)):
        index += 1


def AutoInput():
    index = 0
    for i in range(100000):

        try:
            end = driver.find_elements(
                By.CSS_SELECTOR, ".green-flag_green-flag_1kiAo.green-flag_is-active_2oExT")
            if len(end) == 0:
                break  # 作品のプログラムが終了していれば，スクリーンショット収集終了

            result = getMovement(index)

            # スプライトのX座標Y座標を取得
            for j in positionX:
                print('X: ' + j.get_attribute("value"))
            for j in positionY:
                print('Y: ' + j.get_attribute("value"))

            Inputbox = driver.find_elements(
                By.XPATH, '/html/body/div[1]/div/div[3]/div/div[2]/div[1]/div[2]/div/div[1]/div[1]/canvas')
            print(Inputbox)
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
