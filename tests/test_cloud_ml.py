import os
import sys
import unittest
sys.path.append(os.path.join(os.path.dirname(__file__), "../"))
from jetbull.cloud_ml.client import Client  # noqa
from jetbull.cloud_ml.entity import ModelEntity  # noqa


CREDENTIAL = os.path.join(os.path.dirname(__file__), "../credential.json")


class TestCloudML(unittest.TestCase):

    def test_connect_ml(self):
        client = Client.from_service_account_json(CREDENTIAL)
        model = ModelEntity("test", "test model")
        client.model.create(model)
        models = client.models()
        for m in models:
            print(m)
        client.model.delete(model)


if __name__ == "__main__":
    unittest.main()
