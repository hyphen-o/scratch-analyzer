import numpy as np
import pandas as pd


def numpyToFile(data, path):
    np.savetxt(path, data, delimiter=',')
    print('save numpyFile')


def dfToFile(data, path):
    df = pd.DataFrame(data)
    df.to_csv(path, sep=',', index=False)
    print('save dataframeFile')
