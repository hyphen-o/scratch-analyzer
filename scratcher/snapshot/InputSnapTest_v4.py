import os
import time
import sys
import pandas as pd
import tkinter as tk
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome import service as fs
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from concurrent.futures import ThreadPoolExecutor
from webdriver_manager.chrome import ChromeDriverManager

# ids = pd.read_csv("/Users/socsel/dataset.csv", usecols=["p_ID"], dtype="str")
# retryIds = pd.read_csv("/Users/socsel/retryIds.csv", usecols=["p_ID"], dtype="str")
retryIds = pd.read_csv("out_csv/retryIds.csv",
                       usecols=["p_ID"], dtype="str")
retryIds = list(retryIds)

# キー名と一致するセレニウムキーオプションの辞書
KEY_DICT = {'space': Keys.SPACE,
            'up arrow': Keys.ARROW_UP,
            'down arrow': Keys.ARROW_DOWN,
            'right arrow': Keys.ARROW_RIGHT,
            'left arrow': Keys.ARROW_LEFT,
            'any': Keys.SPACE}

# 作品のASTを取得する
id = sys.argv[1]

df_none = pd.read_csv(f'coordinate_csv/{id}_coordinate.csv')


# chrome_service = fs.Service(
#     "/Users/keigo-o/chromedriver")
driver = webdriver.Chrome(ChromeDriverManager().install())

driver.get("https://scratch.mit.edu/projects/" + str(id) + "/editor")

wait = WebDriverWait(driver, 15)
loadClassName = "loader_bottom-block_1-3rO"

savePath = "./screenshots/" + str(id)
if not os.path.isdir(savePath):
    os.mkdir(savePath)

startTime = time.time()

try:
    wait.until(EC.presence_of_element_located(
        (By.CLASS_NAME, loadClassName)))  # 作品のロード開始を待機
    wait.until_not(EC.presence_of_element_located(
        (By.CLASS_NAME, loadClassName)))  # 作品のロード完了を待機
except TimeoutException as te:
    print(str(id) + ": timeout")  # 作品が存在していないため，スキップ
    driver.close()
    driver.quit()
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

    start = driver.find_elements(
        By.CLASS_NAME, "green-flag_green-flag_1kiAo")

    start[0].click()
    print('start')
    initialflg = False

except Exception as e:
    print(str(id) + ": crash error")  # Scratchがクラッシュするエラー
    print(str(e))
    retryIds.append(str(id))  # エラーが発生した場合，後ほど再試行するためidを配列に追加して保持
    driver.close()
    sys.exit()


def ScreenShot():
    try:
        png = driver.find_element(
            By.CLASS_NAME, "stage-wrapper_stage-canvas-wrapper_3ewmd").screenshot_as_png  # スクリーンショットを取得
        with open(savePath + "/" + str(id) + "-" + str(i) + ".png", "wb") as f:
            f.write(png)
        print("save png: " + str(i))

    except Exception as e:
        print(e)
        driver.close()
        driver.quit()


def ScreenHandler():
    root = tk.Tk()
    for i in range(100):
        root.after(200, ScreenShot)
    driver.close()
    driver.quit()


def sameCoordinate(index):
    actions = ActionChains(driver)
    print(index)
    if ((df_none.iloc[index + 1][1] == df_none.iloc[index - 1][1]) and (df_none.iloc[index + 1][2] == df_none.iloc[index - 1][2])):
        print(df_none.iloc[index + 2][0])
        actions.key_down(
            KEY_DICT[str(df_none.iloc[index + 2][0])]).perform()
        time.sleep(0.1)
        actions.key_up(
            KEY_DICT[str(df_none.iloc[index + 2][0])]).perform()
        if (len(df_none.index - 1) > index + 2):
            return sameCoordinate(index + 2)
        else:
            return index + 1
    else:
        return index + 1


# スクリーンショットを行う関数
index = 0
if not initialflg:
    ScreenHandler()
    initialflg = False
actions = ActionChains(driver)
for i in range(1000000):
    try:
        end = driver.find_elements(
            By.CSS_SELECTOR, ".green-flag_green-flag_1kiAo.green-flag_is-active_2oExT")
        if len(end) == 0:
            break  # 作品のプログラムが終了していれば，スクリーンショット収集終了

        # スプライトのX座標Y座標を取得
        for j in positionX:
            X = j.get_attribute("value")
        for j in positionY:
            Y = j.get_attribute("value")
        print('X: ' + str(X))
        print('Y: ' + str(Y))

        print('path')
        if (df_none.iloc[index][3]):
            print('sleep')
            time.sleep(df_none.iloc[index][3])
            print('wake up')
        print('not wait')
        if (df_none.iloc[index + 1][0] and (abs(round(df_none.iloc[index][1]) - int(X)) < 5 and abs(round(df_none.iloc[index][2]) - int(Y)) < 5)):
            print(df_none.iloc[index + 1][0])
            actions.key_down(
                KEY_DICT[str(df_none.iloc[index + 1][0])]).perform()
            time.sleep(0.1)
            actions.key_up(
                KEY_DICT[str(df_none.iloc[index + 1][0])]).perform()
            if (len(df_none.index - 1) > index + 1):
                index = sameCoordinate(index + 1)
                print(index)

    except Exception as e:
        print(str(id) + ": error")  # 予期せぬエラー
        print(e)
        retryIds.append(str(id))  # エラーが発生した場合，後ほど再試行するためidを配列に追加して保持
        driver.close()
        driver.quit()
        break

# 自動入力を行う関数

elapsedTime = time.time() - startTime
print(str(id) + ": " + str(elapsedTime) + "s")

df = pd.DataFrame(retryIds, columns=["p_ID"])

if len(retryIds) > 1:
    df.to_csv("retryIds.csv")

driver.close()
driver.quit()
