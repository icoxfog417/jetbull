import os
import sys
import unittest
sys.path.append(os.path.join(os.path.dirname(__file__), "../"))
from jtests.sample.model_resource import SampleModelResource  # noqa


class TestModelResource(unittest.TestCase):

    def test_archive(self):
        mr = SampleModelResource()
        package, package_path = mr.archive()
        self.assertTrue(os.path.isfile(package_path))
        os.remove(package_path)


if __name__ == "__main__":
    unittest.main()
