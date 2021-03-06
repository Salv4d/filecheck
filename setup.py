#!/usr/bin/python3
from setuptools import setup, find_packages

setup(
    name="filecheck",
    version="0.0.3",
    description="Verify if a new version of a file is available and update the file if true.",
    author="Salvador Oliveira",
    author_email="slsalvadorlucas@gmail.com",
    py_modules=[""],
    package_dir={"": "src"},
    packages=find_packages(
        include=["filecheck"],
    ),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: MIT License",
        "Operating System :: OS Independent",
    ],
)
