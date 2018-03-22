import os
from io import BytesIO
import pandas as pd
from sklearn.model_selection import train_test_split
from google.cloud import storage


class Datasets():

    def __init__(self, root, client=None):
        self.root = root
        self._client = None
        if client is not None:
            self._client = storage.Client(
                                project=client.project,
                                credentials=client._credentials)

    def resource(self, path, target=""):
        return Resource(self.root, path, target, self._client)


class Resource():

    def __init__(self, root, path, target="", client=None):
        self.root = root
        self.path = path
        self._target = target
        self._client = client
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

    def full_path(self, on_cloud=False):
        if on_cloud:
            base = os.path.basename(self.root)
            return "gs://" + ("/".join([base, self.path]))
        else:
            return os.path.join(self.root, self.path)

    def load(self, on_cloud=False):
        path = self.full_path(on_cloud)
        if on_cloud:
            return self.load_cloud(path)
        else:
            return self.load_local(path)

    def load_local(self, path):
        if not os.path.isfile(path):
            _path = self.full_path(on_cloud=True)
            blob = self._get_blob(_path)
            blob.download_to_filename(path)
        df = pd.read_csv(path)
        self._cache = df
        return self

    def load_cloud(self, path):
        blob = self._get_blob(path)
        string_bytes = blob.download_as_string()
        df = pd.read_csv(BytesIO(string_bytes))
        self._cache = df
        return self

    def _get_blob(self, path):
        drive, prefix = path.split("//")
        bucket, file_path = prefix.split("/", 1)
        bucket = self._client.get_bucket(bucket)
        blob = bucket.get_blob(file_path)
        return blob
