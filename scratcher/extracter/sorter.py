import sys

sys.path.append("../")

import os
from utils import scratchManager, removeExtension

JSON_DIR = sys.path[-1] + "dataset_json"
CSV_DIR = sys.path[-1] + "sorted_csv"


def main():
    for filename in os.listdir(JSON_DIR):
        try:
            id = removeExtension(filename)
            SM = scratchManager(id)
            SM.sortBlocks(CSV_DIR)
        except Exception as e:
            print("ソート中にエラーが発生しました．")
            print(e)
            continue


main()
