import os
import plac
from jetbull.cloud_ml.client import Client
from jtests.sample.datasets import SampleDatasets
from jtests.sample.model_resource import SampleModelResource
from sklearn.ensemble import RandomForestClassifier
from sklearn.externals import joblib


def train(
        on_cloud: ("Execute on Cloud", "flag"),
        credential_path: ("Credential path", "option") = "",
        job_dir: ("Directory for logging", "option", "jd") = "",
        n_estimators: ("number of estimators", "option", None, int) = 50
        ):
    # Prepare data
    client = Client.create(credential_path)
    dataset = client.dataset(SampleDatasets)
    resource = dataset.telecom_data.load(on_cloud=on_cloud)

    # Train
    resource.data.drop(columns=["phone number", "state",
                                "international plan", "voice mail plan"],
                       inplace=True)
    resource.data["churn"] = resource.data["churn"].apply(
                                lambda x: 1 if x else 0)
    train_x, test_x, train_y, test_y = resource.train_test_split()
    model = RandomForestClassifier(n_estimators=n_estimators, oob_score=True)

    model.fit(train_x, train_y)
    print("Done training")

    tmp_path = os.path.join(os.path.dirname(__file__), "temp_model.pkl")
    joblib.dump(model, tmp_path)
    saved_path = client.job(SampleModelResource).store(tmp_path,
                                                       on_cloud=on_cloud)
    print(saved_path)


if __name__ == "__main__":
    plac.call(train)
