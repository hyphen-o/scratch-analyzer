import sys

sys.path.append("../")

import os
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome import service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from concurrent.futures import ThreadPoolExecutor
from webdriver_manager.chrome import ChromeDriverManager

from utils import removeExtension

# ids = pd.read_csv("/Users/socsel/dataset.csv", usecols=["p_ID"], dtype="str")
# retryIds = pd.read_csv("/Users/socsel/retryIds.csv", usecols=["p_ID"], dtype="str")
retryIds = pd.read_csv("../dataset/retryIds.csv", usecols=["p_ID"], dtype="str")
retryIds = list(retryIds)
DIR = "../dataset/result-a_yet.csv"


# スナップショットを実行するメソッド
def snapshot():
    # for id in ids["p_ID"]:

    result_csv = pd.read_csv(DIR)
    num_rows = len(result_csv)

    # for filename in os.listdir(DIR):
    # id = removeExtension(filename)
    try:
        for index, row in result_csv.iterrows():
            driver = webdriver.Chrome(
                service=ChromeService.Service(ChromeDriverManager().install())
            )
            print("driver install")
            id = row["id"]
            print(id)

            driver.get("https://scratch.mit.edu/projects/" + str(id))

            wait = WebDriverWait(driver, 15)
            loadClassName = "loader_bottom-block_1-3rO"

            try:
                wait.until(
                    EC.presence_of_element_located((By.CLASS_NAME, loadClassName))
                )  # 作品のロード開始を待機
                wait.until_not(
                    EC.presence_of_element_located((By.CLASS_NAME, loadClassName))
                )  # 作品のロード完了を待機
            except TimeoutException as te:
                print(str(id) + ": timeout")  # 作品が存在していないため，スキップ
                driver.close()
                continue

            try:
                start = driver.find_elements(
                    By.CLASS_NAME, "green-flag_green-flag_1kiAo"
                )
                start[0].click()
            except Exception as e:
                print(str(id) + ": crash error")  # Scratchがクラッシュするエラー
                print(e)
                retryIds.append(str(id))  # エラーが発生した場合，後ほど再試行するためidを配列に追加して保持
                driver.close()
                continue

            savePath = "../screenshots4/" + str(id)
            if not os.path.isdir(savePath):
                os.mkdir(savePath)

            startTime = time.time()

            for i in range(100):
                time.sleep(0.2)

                try:
                    end = driver.find_elements(
                        By.CSS_SELECTOR,
                        ".green-flag_green-flag_1kiAo.green-flag_is-active_2oExT",
                    )
                    if len(end) == 0:
                        break  # 作品のプログラムが終了していれば，スクリーンショット収集終了
                    png = driver.find_element(
                        By.CLASS_NAME, "stage-wrapper_stage-canvas-wrapper_3ewmd"
                    ).screenshot_as_png  # スクリーンショットを取得
                except Exception as e:
                    print(str(id) + ": error")  # 予期せぬエラー
                    print(e)
                    retryIds.append(str(id))  # エラーが発生した場合，後ほど再試行するためidを配列に追加して保持
                    driver.close()
                    break

                try:
                    with open(
                        savePath + "/" + str(id) + "-" + str(i) + ".png", "wb"
                    ) as f:
                        f.write(png)
                    print("save png: " + str(i))
                except OSError as oe:
                    print("save error")  # 画像保存失敗エラー
                    driver.close()
                    continue

            elapsedTime = time.time() - startTime
            print(str(id) + ": " + str(elapsedTime) + "s")

            df = pd.DataFrame(retryIds, columns=["p_ID"])

            if len(retryIds) > 1:
                df.to_csv("retryIds.csv")

            driver.close()
        driver.quit()
    except Exception as e:
        print(e)


# 並列処理
if __name__ == "__main__":
    with ThreadPoolExecutor(max_workers=3) as executor:
        executor.submit(snapshot)
