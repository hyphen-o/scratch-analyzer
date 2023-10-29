import sys
import os
import pandas as pd
from tqdm import tqdm
sys.path.append('../../')

from prjman import ProjectManager
from utils import remove_extension
from tools import Tracker

SORTED_PATH = sys.path[-1] + "../out/sorted"
DIR_PATH = sys.path[-1] + "../out/tracked/"

for file_name in tqdm(os.listdir(SORTED_PATH)):
    id = remove_extension(file_name)
    df = pd.read_csv(SORTED_PATH + "/" + file_name)
    if len(df.index) < 7:
        print("this project is small")
        continue
    if len(df.index) > 1007:
        df = df.loc[0:1007]
    tracker = Tracker(df)
    tracker.get_coordinate()
    tracker.to_csv(DIR_PATH + file_name)