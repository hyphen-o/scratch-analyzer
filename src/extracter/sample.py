
import sys
sys.path.append('../')

from utils import scratchManager, count_files
import os

DIR_PATH = sys.path[-1] + "dataset_json" 
AVA_PATH = sys.path[-1] + "dataset/available_blocks.csv"

def main():
    start_id = 271065576
    end_id = 500946724
    for id in range(start_id, end_id):
        try:
            SM = scratchManager(id)
            if(SM.isDataset(AVA_PATH) and SM.getBlocksLength() > 1):
                SM.toJson(DIR_PATH)
                print(id)
                # print(count_files(DIR_PATH))
                # if(count_files(DIR_PATH) == 10000):
                #     break
            else:
                print(str(id) + "is not dataset")
        except Exception as e:
            continue
main()

