import os
from jetbull.datasets import Datasets


class SampleDatasets(Datasets):

    def __init__(self, client=None):
        root = os.path.join(os.path.dirname(__file__), "../example-data")
        super().__init__(root, client)

    @property
    def telecom_data(self):
        file_path = "bigml_59c28831336c6604c800002a.csv"
        return self.resource(file_path, target="churn")
