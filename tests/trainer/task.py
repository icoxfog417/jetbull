import os
import plac
from tests.trainer.datasets import TestDatasets
from sklearn.ensemble import RandomForestClassifier


def train(
        on_local: ("Execute on local", "flag"),
        data_root: ("Data root folder", "option") = "example-data",
        output_root: ("Output root folder", "option") = "",
        n_estimators: ("number of estimators", "option", None, int) = 50
        ):
    # Prepare data
    root = os.path.join(os.path.dirname(__file__), data_root)
    dataset = TestDatasets(root)
    resource = dataset.telecom_data.load(on_cloud=not on_local)

    # Train
    resource.data.drop(columns=["phone number", "state",
                                "international plan", "voice mail plan"],
                       inplace=True)
    resource.data["churn"] = resource.data["churn"].apply(lambda x: 1 if x else 0)
    train_x, test_x, train_y, test_y = resource.train_test_split()
    model = RandomForestClassifier(n_estimators=n_estimators, oob_score=True)

    model.fit(train_x, train_y)
    print("Done training")


if __name__ == "__main__":
    plac.call(train)
