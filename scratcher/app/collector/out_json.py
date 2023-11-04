import sys
import os
import pandas as pd
from tqdm import tqdm

sys.path.append("../../")

from prjman import ProjectManager
from utils import remove_extension

DIR_PATH = sys.path[-1] + "../out/new_dataset/"
TRACKER_PATH = sys.path[-1] + "../out/tracked"
ID_PATH = sys.path[-1] + "../out/ids/dataset.csv"

df = pd.read_csv(ID_PATH)
length = len(df.index)
print(length)

for file_name in tqdm(os.listdir(TRACKER_PATH)):
    id = remove_extension(file_name)
    pm = ProjectManager(id)
    pm.to_json(DIR_PATH)
