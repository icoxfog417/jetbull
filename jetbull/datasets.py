import os
from io import BytesIO
import pandas as pd
from sklearn.model_selection import train_test_split
from google.cloud import storage
from jetbull.jet_template import JetTemplate


class Datasets(JetTemplate):

    def __init__(self, root, credential_path=""):
        super().__init__(credential_path)
        self.root = root

    def resource(self, path, target=""):
        return Resource(self.root, path, self.credential_path, target)


class Resource(JetTemplate):

    def __init__(self, root, path, credential_path, target=""):
        super().__init__(credential_path)
        self.root = root
        self.path = path
        self._target = target
        self._cache = None

    @property
    def data(self):
        return self._cache

    @property
    def features(self):
        if self._target:
            return self.data.drop(columns=[self._target])
        else:
            return self.data

    @property
    def target(self):
        if self._target:
            return self.data[self._target]
        else:
            return None

    def split_target(self):
        if self._target:
            return (self.data.drop(columns=[self._target]),
                    self.data[self._target],)
        else:
            return (self.data, None)

    def train_test_split(self, test_size=0.25, random_state=None):
        X, y = self.split_target()
        return train_test_split(X, y, test_size=test_size,
                                random_state=random_state)

    def get_client(self):
        if self.credential_path:
            return storage.Client.from_service_account_json(
                    self.credential_path)
        else:
            return storage.Client()

    def full_path(self, on_cloud=False):
        if on_cloud:
            base = os.path.basename(self.root)
            return "gs://" + ("/".join([base, self.path]))
        else:
            return os.path.join(self.root, self.path)

    def load(self, on_cloud=False):
        path = self.full_path(on_cloud)
        func = self.jet(on_cloud, self.load_cloud, self.load_local)
        return func(path)

    def load_local(self, path):
        df = pd.read_csv(path)
        self._cache = df
        return self

    def load_cloud(self, path):
        client = self.get_client()
        drive, prefix = path.split("//")
        bucket, file_path = prefix.split("/", 1)
        bucket = client.get_bucket(bucket)
        blob = bucket.get_blob(file_path)
        string_bytes = blob.download_as_string()
        df = pd.read_csv(BytesIO(string_bytes))
        self._cache = df
        return self
