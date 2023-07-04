import pandas as pd

class DfManager:
    def __init__(self, rowName):
        self.__df = pd.DataFrame(columns=rowName)
        self.__ROWNAME = rowName

    def get_df(self):
        return self.__df
    
    def add_row(self, row):
        row = pd.DataFrame([row], columns=self.__ROWNAME)
        self.__df = pd.concat([self.__df, row])

    def to_csv(self, dir_path):
        self.__df.to_csv(dir_path)
        

