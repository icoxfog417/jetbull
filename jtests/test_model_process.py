import os
import sys
import unittest
from sklearn import datasets
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import QuantileTransformer
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
sys.path.append(os.path.join(os.path.dirname(__file__), "../"))
from jetbull.model_process import ModelProcess  # noqa


class TestModelProcess(unittest.TestCase):

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
        pipe.train(train_x, train_y)

        preds = pipe.predict(test_x)
        print(classification_report(test_y, preds))


if __name__ == "__main__":
    unittest.main()
