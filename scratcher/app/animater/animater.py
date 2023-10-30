import sys
import os
from tqdm import tqdm
import pandas as pd

sys.path.append("../../")

from tslearn.preprocessing import TimeSeriesScalerMinMax
from tslearn.utils import to_time_series_dataset

from prjman import ProjectManager
from config import constants
from utils import DfManager, parallel_runner, remove_extension
from animation import Animater
from dtw import DTW

for file_name in tqdm(os.listdir("../../out/tracked")):
    df = pd.read_csv(f"../../out/tracked/{file_name}")
    if len(df.index) > 100:
        print("too long")
        df = df.loc[0:100]
    id = remove_extension(file_name)
    data = (
        TimeSeriesScalerMinMax()
        .fit_transform(to_time_series_dataset([df[["x", "y"]].values.tolist()]))
        .flatten()
        .reshape(-1, 2)
    )
    animater = Animater(data)
    print("animate")
    animater.generate_gif(f"../../out/animations/{id}.gif")
    print("animate")
    continue
