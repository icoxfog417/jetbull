import os
from setuptools import setup, find_packages


requires = []
if os.path.isfile("requirements.txt"):
    with open("requirements.txt") as f:
        requires = f.read().splitlines()


setup(
    name="demo-model",
    install_requires=requires,
    packages=find_packages(exclude=("jtests")),
    data_files=[("", ["requirements.txt"])]
)
