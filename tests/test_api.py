import os
import sys
import unittest
import numpy as np
from sklearn import datasets
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import QuantileTransformer
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
sys.path.append(os.path.join(os.path.dirname(__file__), "../"))
from jetbull.model_process import ModelProcess  # noqa
from jetbull.threshold_estimator import ThresholdEstimator # noqa
from jetbull.api import API # noqa


class TestAPI(unittest.TestCase):

    def test_process(self):
        # Prepare the trained model
        iris = datasets.load_iris()
        X = iris.data
        y = iris.target
        train_x, test_x, train_y, test_y = train_test_split(X, y,
                                                            test_size=0.3)

        # Make pipeline
        preprocessor = QuantileTransformer(random_state=0)
        model = LogisticRegression()
        pipe = ModelProcess([
            ("preprocess", preprocessor),
            ("model", model)
        ])

        # Define API
        iris_th_ranges = [
            np.arange(0.2, 0.8, 0.1),
            np.arange(0.2, 0.8, 0.1),
            np.arange(0.2, 0.8, 0.1)
        ]
        api = API(ThresholdEstimator, iris_th_ranges, "f1_micro")

        # Train the model
        pipe.train(train_x, train_y)

        # Update API
        api.update(pipe, test_x, test_y)  # then, serialize

        preds = api.predict(test_x)
        print(classification_report(test_y, preds))
        print(api.thresholds)


if __name__ == "__main__":
    unittest.main()
