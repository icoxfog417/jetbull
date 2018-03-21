import os
import sys
import shutil
import unittest
sys.path.append(os.path.join(os.path.dirname(__file__), "../"))
from jetbull.cloud_ml.client import Client  # noqa
from jetbull.cloud_ml.job_client import Packager  # noqa
from jetbull.cloud_ml.entity import JobEntity  # noqa


CREDENTIAL = os.path.join(os.path.dirname(__file__), "../credential.json")


class TestJob(unittest.TestCase):

    def test_packaging(self):
        root = os.path.join(os.path.dirname(__file__), "../")
        pkg = Packager(root)
        package, package_path = pkg.archive("tests/trainer")
        print(package_path)
        self.assertTrue(os.path.isfile(package_path))
        shutil.rmtree(os.path.dirname(package_path))

    def test_get_jobs(self):
        client = Client.from_service_account_json(CREDENTIAL)
        jobs = client.jobs("jetbull-ml")
        for j in jobs:
            print(j)

    def test_create_job(self):
        client = Client.from_service_account_json(CREDENTIAL)
        # Use your bucket for training the model
        job_client = client.job("jetbull-ml")
        created = job_client.create(
            trainer_root=os.path.join(os.path.dirname(__file__), "../"),
            trainer_module="tests.trainer.task",
            trainer_args=("-n-estimators", "40"),
            region="asia-east1"
        )
        self.assertTrue(created)


if __name__ == "__main__":
    unittest.main()
