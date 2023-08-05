#!/usr/bin/env python3
# coding: utf-8

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="zen_fillet",
    version="1.0.0",
    author="Mark Zorikhin",
    author_email="hnau256@gmail.com",
    description="Util to calculate fillet or chamfer radius by reducing or reducing by radius",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/hnau_zen/fillet",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)