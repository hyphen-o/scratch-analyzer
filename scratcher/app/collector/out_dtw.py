import sys
import os
import csv
from tqdm import tqdm
import pandas as pd

sys.path.append("../../")

from tslearn.preprocessing import TimeSeriesScalerMinMax
from tslearn.utils import to_time_series_dataset

from dtw import DTW
from prjman import ProjectManager
from config import constants
from utils import DfManager, parallel_runner, remove_extension
from animation import Animater

PATH = "../../out/dtw/dtw.csv"
with open(PATH, "w") as f:
    writer = csv.writer(f)
    writer.writerow(["id1", "id2", "dtw"])

Dtw = DTW()
with open(PATH, "a") as f:
    for file_name1 in tqdm(os.listdir("../../out/tracked")):
        for file_name2 in tqdm(os.listdir("../../out/tracked")):
            if file_name1 == file_name2:
                continue
            df1 = pd.read_csv(f"../../out/tracked/{file_name1}")
            df2 = pd.read_csv(f"../../out/tracked/{file_name2}")
            if len(df1) > 100:
                df1 = df1.loc[0:100]
            if len(df2) > 100:
                df2 = df2.loc[0:100]
            if len(df1) < 4:
                continue
            if len(df2) < 4:
                continue
            id1 = remove_extension(file_name1)
            id2 = remove_extension(file_name2)
            # data1 = TimeSeriesScalerMinMax().fit_transform(
            #             to_time_series_dataset([df1[["x", "y"]].values.tolist()])).flatten().reshape(-1, 2)
            # data2 = TimeSeriesScalerMinMax().fit_transform(
            #             to_time_series_dataset([df2[["x", "y"]].values.tolist()])).flatten().reshape(-1, 2)
            if len(df1.index) == 1 and len(df2.index) == 1:
                continue
            Dtw.set_dtw(
                df1[["x", "y"]].values.tolist(), df2[["x", "y"]].values.tolist()
            )
            value = Dtw.get_dtw()
            writer = csv.writer(f)
            writer.writerow([id1, id2, value])
