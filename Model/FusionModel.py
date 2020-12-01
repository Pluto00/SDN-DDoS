import os
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn import metrics
from collections import Counter
from Model.Dataset import Dataset
from Model.BaseModel import BaseModel, SVCModel, RFCModel, DTCModel, KNCModel, GNBModel
import joblib


class FusionModel(BaseModel):
    MODEL_COUNT = 5

    def __init__(self, is_train=False, name='FM', pre_path='', path='models/', **kwargs):
        super().__init__(name, **kwargs)
        self.__pre_path = pre_path
        self.__path = pre_path + path
        self.__train = is_train
        self.train_X, self.test_X, self.train_Y, self.test_Y = None, None, None, None
        self.scale = StandardScaler()
        if is_train:
            self.models = [SVCModel(), RFCModel(), DTCModel(), KNCModel(), GNBModel()]
        else:
            self.scale = None
            self.models = []
            self.__load()
            if len(self.models) != FusionModel.MODEL_COUNT:
                raise Exception("WRONG NUMBER OF MODELS!!!")

    def load_data(self, dataset, count=3500, test_size=0.1, random_state=42):
        data = Dataset(dataset, count)
        self.train_X, self.test_X, self.train_Y, self.test_Y = train_test_split(
            data.getX(),
            data.getY(),
            test_size=test_size,
            random_state=random_state
        )
        # self.scale.fit(data.getX())
        del data

    def __preprocess(self, data):
        return self.scale.fit_transform(data)

    def __load(self):
        print("Fusion Model is loading...")
        for filename in os.listdir(self.__path):
            self.models.append(joblib.load(self.__path + filename))
        self.scale = joblib.load(self.__pre_path + 'scaler.model')

    def __save(self):
        for model in self.models:
            model.save(self.__path)
        joblib.dump(self.scale, self.__pre_path + 'scaler.model')

    def train(self):
        if not self.__train:
            raise Exception("NOT ALLOWED TRAIN!!!")
        for model in self.models:
            model.fit(self.__preprocess(self.train_X), self.train_Y)
            pred_Y = model.predict(self.__preprocess(self.test_X))
            model.score = metrics.accuracy_score(self.test_Y, pred_Y)
        self.__save()

    def predict(self, x):
        x = self.__preprocess(x)
        results = np.concatenate([model.predict(x) for model in self.models]).reshape(FusionModel.MODEL_COUNT, -1).T
        return np.array([Counter(result).most_common(1)[0][0] for result in results])
