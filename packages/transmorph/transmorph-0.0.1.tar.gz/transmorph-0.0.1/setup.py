#!/usr/bin/env python3
#
import setuptools

with open("Readme.org", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="transmorph",  # Replace with your own username
    version="0.0.1",
    author="Aziz Fouché",
    author_email="aziz.fouche@curie.fr",
    description="Optimal transport-based tools for data integration.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Risitop/transmorph",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'numpy',
        'pot',
        'scipy',
        'osqp',
    ],
    python_requires=">=3.6",
)
