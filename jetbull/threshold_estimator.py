from collections import OrderedDict
import numpy as np
from sklearn.base import BaseEstimator, ClassifierMixin
from sklearn.model_selection import ParameterGrid
from sklearn.utils.validation import check_X_y, check_array
from sklearn.utils.multiclass import unique_labels
from sklearn.metrics.scorer import check_scoring
from sklearn.preprocessing import OneHotEncoder


class ThresholdEstimator(BaseEstimator, ClassifierMixin):

    def __init__(self, model=None, threshold_or_thresholds=0.5):
        self.model = model
        self.thresholds = threshold_or_thresholds
        if self.thresholds is None:
            self.thresholds = 0.5
        if not isinstance(self.thresholds, (tuple, list)):
            self.thresholds = [self.thresholds, 1 - self.thresholds]
        elif len(self.thresholds) == 1:
            th = self.thresholds[0]
            self.thresholds = [th, 1 - th]
        self.thresholds = np.array(self.thresholds)

    def fit(self, X, y):
        if not (hasattr(self.model, "predict_proba") or
                hasattr(self.model, "predict")):
            raise Exception("Model does not have predict/predict_proba method")
        X, y = check_X_y(X, y)
        self.classes_ = unique_labels(y)
        return self

    def predict(self, X):
        if hasattr(self.model, "predict_proba"):
            preds = self.model.predict_proba(X)
        else:
            preds = self.model.predict(X)

        mask = preds >= self.thresholds
        clipped = np.zeros(preds.shape)
        clipped[mask] = 1
        return clipped

    @classmethod
    def estimate(cls, model, X, y, threshold_ranges, scoring=None):
        # make parameters
        ranges = OrderedDict()
        keys = []
        for i, r in enumerate(threshold_ranges):
            key = "th_{}".format(i)
            ranges[key] = r
            keys.append(key)
        grid = ParameterGrid(ranges)
        thresholds = []
        for p in grid:
            ts = [p[k] for k in keys]
            thresholds.append(ts)

        # execute grid search
        enc = OneHotEncoder()
        _y = y
        if isinstance(y, (list, tuple)):
            _y = np.array(y).reshape((-1, 1))
        elif len(y.shape) < 2:
            _y = np.array(y).reshape((-1, 1))
        y_true = enc.fit_transform(_y).toarray()
        estimator = cls(model)
        scorer = check_scoring(estimator, scoring=scoring)
        best_score = -1
        best_model = None
        for th in thresholds:
            estimator = cls(model, th)
            score = scorer(estimator, X, y_true)
            if best_score < score:
                best_score = score
                best_model = estimator

        return best_model
