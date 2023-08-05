import setuptools
from setuptools import version
from pathlib import Path

setuptools.setup(
    name="issypdf",
    version=1.0,
    long_description=Path("README.md").read_text(),
    package=setuptools.find_packages(exclude=["tests", "data"])
)
