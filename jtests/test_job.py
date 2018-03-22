import os
import sys
import shutil
import unittest
sys.path.append(os.path.join(os.path.dirname(__file__), "../"))
from jetbull.cloud_ml.client import Client  # noqa
from jtests.sample.model_resource import SampleModelResource
from jetbull.cloud_ml.entity import JobEntity  # noqa


CREDENTIAL = os.path.join(os.path.dirname(__file__), "../credential.json")


class TestJob(unittest.TestCase):

    def xtest_get_jobs(self):
        client = Client.from_service_account_json(CREDENTIAL)
        jobs = client.jobs()
        for j in jobs:
            print(j)

    def xtest_train_local(self):
        client = Client.from_service_account_json(CREDENTIAL)
        # Use your bucket for training the model
        job = client.job(SampleModelResource)
        created = job.train(
            trainer_module="jtests.sample.trainer.task",
            trainer_args=(
                "-credential-path", CREDENTIAL,
                "-n-estimators", "40"
                ),
            region="asia-east1"
        )
        self.assertTrue(created)

    def test_train_cloud(self):
        client = Client.from_service_account_json(CREDENTIAL)
        job = client.job(SampleModelResource)
        created = job.train(
            trainer_module="jtests.sample.trainer.task",
            trainer_args=(
                "-n-estimators", "40"
                ),
            region="asia-east1", on_cloud=True
        )
        self.assertTrue(created)


if __name__ == "__main__":
    unittest.main()
