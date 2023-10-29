import sys
import pandas as pd
from tqdm import tqdm
sys.path.append('../../')

from prjman import ProjectManager

DIR_PATH = sys.path[-1] + "../out/sorted/"
ID_PATH = sys.path[-1] + "../out/ids/dataset.csv"

df = pd.read_csv(ID_PATH)
length = len(df.index)
print(length)

for index in tqdm(range(1508, length)):
    id = df["id"].iloc[index]
    print(id)
    pm = ProjectManager(id)
    pm.get_sorted_blocks(DIR_PATH + str(id) + ".csv")

