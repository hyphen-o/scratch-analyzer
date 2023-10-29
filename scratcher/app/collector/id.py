import sys
import random
import csv
import numpy as np
sys.path.append('../../')

from prjman import ProjectManager
from config import constants
from utils import DfManager, parallel_runner

CSV_PATH = sys.path[-1] + "../out/sample/id.csv"
# id_list = list(range(276660763,915471041))
random_ids = random.randrange(276660763,915471041, 10000)
random_ids = np.random.randint(low=276660763, high=915471041, size=(5000000))

with open(CSV_PATH, 'w') as f:
    writer = csv.writer(f)
    writer.writerow(["id"])
# dfM = DfManager(["id"])
count = 0
    
def callback(start_index, end_index):
    with open(CSV_PATH, 'a') as f:
        for index in range(start_index, end_index):
            try:
                global count
                id = random_ids[index]
                pm = ProjectManager(id)
                blocks = pm.get_blocks()
                dupli_blocks = []
                has_dupli = False
                has_coordinate = False
                for block_hash, block in blocks.items():
                    block_name = block["opcode"]
                    if block_name in constants.EVENT_BLOCKS:
                        if block_name in dupli_blocks:
                            has_dupli = True
                            break
                        else:
                            dupli_blocks.append(block_name)
                    if block_name in constants.COORDINATE_BLOCKS:
                        has_coordinate = True
                if not has_dupli and has_coordinate:
                    count += 1
                    print(count)
                    print(id)
                    writer = csv.writer(f)
                    writer.writerow([id])
                if count == 4000:
                    break
            except Exception as e:
                print(e)
                continue

print("pararell")
parallel_runner(callback, 5, [[0, 10000], [10001, 20000], [20001, 30000], [30001, 40000], [40001, 50000]])
# parallel_runner(callback, 1, [[0, 100]])

print("pararell")
# dfM.to_csv(CSV_PATH)