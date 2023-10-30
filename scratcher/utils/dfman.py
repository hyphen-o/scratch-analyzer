import pandas as pd


class DfManager:
    def __init__(self, data):
        if isinstance(data, str):
            self.__df = pd.read_csv(data)
            # 列名を配列で取得
            self.__ROWNAME = self.__df.columns.tolist()
        elif isinstance(data, list):
            self.__df = pd.DataFrame(columns=data)
            self.__ROWNAME = data
        else:
            print("Unknown type.")

    def get_df(self):
        return self.__df

    def add_row(self, row):
        row = pd.DataFrame([row], columns=self.__ROWNAME)
        self.__df = pd.concat([self.__df, row], ignore_index=True)

    def sort_row(self, column):
        self.__df = self.__df.sort_values(column)
        return self.__df

    def to_csv(self, dir_path):
        self.__df.to_csv(dir_path)
