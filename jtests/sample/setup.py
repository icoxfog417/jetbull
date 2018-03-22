import os
from setuptools import setup, find_packages


requires = []
if os.path.isfile("requirements.txt"):
    with open("requirements.txt") as f:
        requires = f.read().splitlines()


setup(
    name="sample",
    install_requires=requires,
    packages=find_packages(exclude=("demo", "notebooks", "test_*.py")),
    data_files=[("", ["requirements.txt"])]
)
