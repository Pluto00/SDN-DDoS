from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
import joblib


class BaseModel:
    def __init__(self, name, **kwargs):
        self.model = None
        self.name = name
        self.score = 0

    def fit(self, x, y):
        self.model.fit(x, y)

    def predict(self, x):
        return self.model.predict(x)

    def save(self, path=''):
        joblib.dump(self.model, f'{path}{self.name}_{self.score}.model')

    def __repr__(self):
        return "<%s>: %s" % (self.name, self.score)


class SVCModel(BaseModel):
    def __init__(self, name='SVC', **kwargs):
        super().__init__(name, **kwargs)
        self.model = SVC(kernel='rbf', verbose=0, C=0.1, degree=3, gamma=1, coef0=0.0, shrinking=True,
                         probability=False, tol=1e-3, cache_size=200, class_weight=None,
                         max_iter=-1, decision_function_shape='ovr', break_ties=False, random_state=None)


class RFCModel(BaseModel):
    def __init__(self, name='RFC', **kwargs):
        super().__init__(name, **kwargs)
        self.model = RandomForestClassifier(n_estimators=10, criterion='gini', max_depth=None, min_samples_split=2,
                                            min_samples_leaf=1, min_weight_fraction_leaf=0.0,
                                            max_features='auto', max_leaf_nodes=None, min_impurity_decrease=0.0,
                                            min_impurity_split=None, bootstrap=True, oob_score=False, n_jobs=1,
                                            random_state=None, verbose=0, warm_start=False, class_weight=None)


class DTCModel(BaseModel):
    def __init__(self, name='DTC', **kwargs):
        super().__init__(name, **kwargs)
        self.model = DecisionTreeClassifier(criterion="gini", splitter="best", max_depth=None, min_samples_split=2,
                                            min_samples_leaf=1, min_weight_fraction_leaf=0., max_features=None,
                                            random_state=None, max_leaf_nodes=None, min_impurity_decrease=0.,
                                            min_impurity_split=None, class_weight=None, presort='deprecated',
                                            ccp_alpha=0.0)


class KNCModel(BaseModel):
    def __init__(self, name='KNC', **kwargs):
        super().__init__(name, **kwargs)
        self.model = KNeighborsClassifier(n_neighbors=5, weights='uniform', algorithm='auto', leaf_size=30,
                                          p=2, metric='minkowski', metric_params=None, n_jobs=None, )


class GNBModel(BaseModel):
    def __init__(self, name='GNB', **kwargs):
        super().__init__(name, **kwargs)
        self.model = GaussianNB(priors=None, var_smoothing=1e-9)
