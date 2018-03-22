import os
import plac
from sklearn.metrics import classification_report
from sklearn.externals import joblib
from jetbull.cloud_ml.client import Client
from jetbull.model_process import ModelProcess
from demo.datasets import DemoDatasets
from demo.model_resource import DemoModelResource
from demo.preprocessor import ColumnEncoder, DropColumn, CategoricalToNumerical
from demo.model import make_model
from demo.api import api


def train(
        on_cloud: ("Execute on Cloud", "flag"),
        credential_path: ("Credential path", "option") = "",
        job_dir: ("Directory for logging", "option", "jd") = "",
        n_estimators: ("number of estimators", "option", None, int) = 50
        ):
    # Prepare data
    client = Client.create(credential_path)
    dataset = client.dataset(DemoDatasets)
    resource = dataset.telecom_data.load(on_cloud=on_cloud)

    # Make model training pipeline
    model = make_model(n_estimators)
    pipe = ModelProcess([
        ("delete phone number", DropColumn("phone number")),
        ("state encoding", ColumnEncoder("state")),
        ("international plan conversion",
         CategoricalToNumerical("international plan", {"yes": 1, "no": 0})),
        ("voice mail plan conversion",
         CategoricalToNumerical("voice mail plan", {"yes": 1, "no": 0})),
        ("churn", CategoricalToNumerical("churn", {True: 1, False: 0})),
        ("model", model)
    ])

    # Train
    train_x, test_x, train_y, test_y = resource.train_test_split()
    pipe.train(train_x, train_y)

    preds = pipe.predict(test_x)
    print("Evaluate the Model")
    print(classification_report(test_y, preds))

    tmp_path = os.path.join(os.path.dirname(__file__), "temp_model.pkl")
    joblib.dump(model, tmp_path)
    saved_path = client.job(DemoModelResource).store(tmp_path,
                                                     on_cloud=on_cloud)
    print(saved_path)

    """
    api.update(pipe, test_x, test_y)
    print("Update API threshold")
    print(api.thresholds)
    """


if __name__ == "__main__":
    plac.call(train)
