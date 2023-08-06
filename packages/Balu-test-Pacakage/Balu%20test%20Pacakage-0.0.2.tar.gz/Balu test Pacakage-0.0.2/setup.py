import os
import setuptools
from setuptools import setup

setup(
    name="Balu test Pacakage",
    version="0.0.2",
    author="Balaji Chippada",
    author_email="BALAJI.CHIPPADA@t-systems.com",
    description=("An demonstration of how to create, document, and publish "
                                   "to the cheese shop a5 pypi.org."),
    license="BSD",
    keywords="example documentation tutorial",
    url="http://packages.python.org/an_example_pypi_project",
    packages=setuptools.find_packages(),
    long_description="",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],
)

