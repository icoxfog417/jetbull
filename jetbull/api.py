import json
import numpy as np
from jetbull.datasets import Resource


class API():

    def __init__(self, threshold_class=None,
                 threshold_ranges=(), scoring=None):
        self.threshold_class = threshold_class
        self.threshold_ranges = threshold_ranges
        self.scoring = scoring
        self._threshold = None

    def save(self, threshold_path):
        with open(threshold_path, "wb") as f:
            f.write(json.dumps({
                "threshold": self._threshold.thresholds
            }))

    @classmethod
    def load(cls, model, threshold_class, threshold_path):
        with open(threshold_path, encoding="utf-8") as f:
            th = json.load(f)
            value = th["threshold"]
        threshold = threshold_class(model, value)
        instance = cls()
        instance._threshold = threshold
        return instance

    def update(self, model_proc, X, y=None):
        self.model_proc = model_proc
        _X = X
        _y = y
        if y is None:
            if isinstance(X, Resource):
                _X, _y = X.split_target()
            else:
                raise Exception("y is not specified.")

        self._threshold = self.threshold_class.estimate(
                            self.model_proc, _X, _y,
                            self.threshold_ranges, self.scoring)
        return self

    def predict_proba(self, X):
        if self._threshold is None:
            raise Exception("Threshold does not exist.")
        return self._threshold.predict(X)

    def predict(self, X):
        preds = self.predict_proba(X)
        return np.argmax(preds, axis=1)

    @property
    def thresholds(self):
        if self._threshold is None:
            return None
        else:
            return self._threshold.thresholds
