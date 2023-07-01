
import sys
sys.path.append('../')

from utils import scratchManager, count_files
import os
from concurrent.futures import ThreadPoolExecutor

DIR_PATH = sys.path[-1] + "dataset_json" 
AVA_PATH = sys.path[-1] + "dataset/available_blocks.csv"

def main(start_id, end_id):
    for id in range(start_id, end_id):
        try:
            SM = scratchManager(id)
            duplication = []
            if(SM.isDataset(AVA_PATH) and SM.getBlocksLength() > 4):
                print('get')
                flg = False
                for block_hash, blocks in SM.getBlocks().items():
                    block_name = blocks['opcode']
                    if ('event' in block_name):
                        if (block_name in duplication):
                            print('並列に同じイベントブロックが存在します．')
                            flg = True
                            break
                        else:
                            duplication.append(block_name)
                            continue
                if(not flg):
                    SM.toJson(DIR_PATH)

                print(id)

                print(count_files(DIR_PATH))
                # if(count_files(DIR_PATH) == 10000):
                #     break
            else:
                print(str(id) + "is not dataset")
        except Exception as e:
            continue

if __name__ == '__main__':
    with ThreadPoolExecutor(max_workers=3) as executor:
        executor.submit(main, 271002000, 400002000)
        executor.submit(main, 400002001, 500002000)
        executor.submit(main, 500002001, 726797902)
