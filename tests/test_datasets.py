import os
import unittest
from google.cloud import storage


CREDENTIAL = os.path.join(os.path.dirname(__file__), "../credential.json")


class TestStorageAccess(unittest.TestCase):

    def test_get_buckets(self):
        client = storage.Client.from_service_account_json(CREDENTIAL)
        bucket = client.get_bucket("example-data")
        blob = bucket.get_blob("bigml_59c28831336c6604c800002a.csv")
        self.assertTrue(blob)
