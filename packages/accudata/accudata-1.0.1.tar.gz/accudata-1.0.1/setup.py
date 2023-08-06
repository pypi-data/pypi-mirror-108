# -*- coding: utf-8 -*-
"""
Created on Sat Jun  5 01:09:24 2021

@author: Pavel Gostev
"""
import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="accudata",
    version="1.0.1",
    author="Pavel Gostev",
    author_email="gostev.pavel@physics.msu.ru",
    description="Simple module to store data with arbitrary structure in dict or Pandas DataFrame",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/vongostev/accudata",
    packages=setuptools.find_packages(exclude=("tests", )),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    include_package_data=True,
    install_requires=[
        'numpy',
        'pandas'
    ],
)
