import os
from jetbull.datasets import Datasets  # noqa


class MyDatasets(Datasets):

    def __init__(self, root):
        credential = os.path.join(os.path.dirname(__file__),
                                  "../credential.json")
        super().__init__(root, credential)

    @property
    def telecom_data(self):
        file_path = "bigml_59c28831336c6604c800002a.csv"
        return self.resource(file_path, target="churn")
