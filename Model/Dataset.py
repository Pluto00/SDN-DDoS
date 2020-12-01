import pandas as pd
import numpy as np


class Dataset:
    COLUMNS = ['Flow Duration', 'Flow Bytes/s', 'Flow Packets/s',
               'Flow IAT Mean', 'Flow IAT Std', 'Flow IAT Max', 'Flow IAT Min',
               'Fwd IAT Mean', 'Fwd IAT Std', 'Fwd IAT Max', 'Fwd IAT Min',
               'Bwd IAT Mean', 'Bwd IAT Std', 'Bwd IAT Max', 'Bwd IAT Min',
               'Active Mean', 'Active Std', 'Active Max', 'Active Min',
               'Idle Mean', 'Idle Std', 'Idle Max', 'Idle Min']

    def __init__(self, filepath, count=None):
        df = pd.concat([pd.read_csv(path, low_memory=False)[:count] for path in filepath])
        rename_df = df.rename(columns=lambda x: x.strip())
        self.__data = rename_df[~rename_df.isin([np.nan, np.inf, -np.inf]).any(1)]
        self.__x = None
        self.__y = None

    def getY(self):
        if self.__x is None:
            self.__x = self.__data['Label']
        return self.__x

    def getX(self):
        if self.__y is None:
            self.__y = self.__data.loc[:, Dataset.COLUMNS]
        return self.__y

    def getData(self):
        return self.__data

    def setLabel(self, label):
        self.__data['Label'] = label

    def getSrcIp(self, label):
        return self.__data[self.__data['Label'] == label]['Src IP'].unique()


if __name__ == '__main__':
    data = Dataset(['./dataset/attack_syn.csv', './dataset/normal.csv'])
    print(data.getX())
    print(data.getY())
