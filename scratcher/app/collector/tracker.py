import sys
import pandas as pd
from tqdm import tqdm
sys.path.append('../../')

from prjman import ProjectManager

SORTED_PATH = sys.path[-1] + "../out/sorted/"

df = pd.read_csv(ID_PATH)
length = len(df.index)
print(length)

for index in tqdm(range(346, length)):
    id = df["id"].iloc[index]
    pm = ProjectManager(id)
    pm.get_sorted_blocks(DIR_PATH + str(id) + ".csv")