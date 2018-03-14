import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), "../"))
from jetbull.datasets import Datasets


class MyDatasets(Datasets):

    def __init__(self, root):
        credential = os.path.join(os.path.dirname(__file__),
                                  "../credential.json")
        super().__init__(root, credential)

    @property
    def telecom_data(self):
        file_path = "bigml_59c28831336c6604c800002a.csv"
        return self.resource(file_path)


def main():
    root = os.path.join(os.path.dirname(__file__), "example-data")
    if not os.path.exists(root):
        os.mkdir(root)
        sample_file = os.path.join(root, "bigml_59c28831336c6604c800002a.csv")
        with open(sample_file, mode="w", encoding="utf-8") as f:
            f.write(",".join(["Tom", "1", "30"]) + "\n")
            f.write(",".join(["Anne", "0", "60"]) + "\n")

    datasets = MyDatasets(root)

    # from local
    print("Here is local data")
    data = datasets.telecom_data.load()
    print(data.head(3))

    print("Here is cloud data")
    data = datasets.telecom_data.load(on_cloud=True)
    print(data.head(5))


if __name__ == "__main__":
    main()
