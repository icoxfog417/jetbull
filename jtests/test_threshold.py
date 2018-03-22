import os
import sys
import unittest
import numpy as np
from sklearn import datasets
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
sys.path.append(os.path.join(os.path.dirname(__file__), "../"))
from jetbull.threshold_estimator import ThresholdEstimator  # noqa


class TestThreshold(unittest.TestCase):

    def test_threshold(self):
        # Prepare the trained model
        cancer = datasets.load_breast_cancer()
        X = cancer.data
        y = cancer.target
        train_x, test_x, train_y, test_y = train_test_split(X, y,
                                                            test_size=0.3)
        model = LogisticRegression()
        model.fit(train_x, train_y)
        # Estimate the threshold
        cancer_th_ranges = [
            np.arange(0.2, 0.8, 0.1)
        ]
        threshold = ThresholdEstimator.estimate(
                        model, test_x, test_y, cancer_th_ranges)
        print(threshold)

    def test_multiclass_threshold(self):
        # Prepare the trained model
        iris = datasets.load_iris()
        X = iris.data
        y = iris.target
        train_x, test_x, train_y, test_y = train_test_split(X, y,
                                                            test_size=0.3)
        model = LogisticRegression()
        model.fit(train_x, train_y)
        # Estimate the threshold
        iris_th_ranges = [
            np.arange(0.2, 0.8, 0.1),
            np.arange(0.2, 0.8, 0.1),
            np.arange(0.2, 0.8, 0.1)
        ]
        threshold = ThresholdEstimator.estimate(
                        model, test_x, test_y, iris_th_ranges, "f1_micro")
        print(threshold)


if __name__ == "__main__":
    unittest.main()
