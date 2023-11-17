import numpy as np
import pandas as pd
import random
import scipy.stats as stats
import os

TRACK_CSV = '../../out/tracked/'

li = []
for file_name in os.listdir(TRACK_CSV):
  df = pd.read_csv(TRACK_CSV + file_name)
  li.append(len(df.index))

# # 中央値を計算
q1 = np.percentile(li, 25)
q3 = np.percentile(li, 75)
median = np.median(li)
print(q1)
print(median)
print(q3)


