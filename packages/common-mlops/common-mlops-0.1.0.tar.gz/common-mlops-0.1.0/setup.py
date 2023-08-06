#! /usr/bin/env python

import pathlib
from setuptools import find_packages, setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setup(
    name="common-mlops",
    version="0.1.0",
    description="Utilities of MLOps for INRIA",
    long_description=README,
    long_description_content_type="text/markdown",
    author="Patricio Merino",
    author_email="patricio.merino@inria.cl",
    license='MIT',
    url="https://gitlab.com/Inria-Chile/common-mlops",
    packages=find_packages(exclude=("test",)),
    include_package_data=True,
    download_url="https://gitlab.com/Inria-Chile/common-mlops/archive/v{version}"
    ".tar.gz".format(version="0.1.0"),
    install_requires=['boto3>=1.17.27', 'pandas>=1.2.3', 'gitdb2>=4.0.2', 'dvc>=2.0.1', 's3-streaming>=0.0.3', 'smart_open>=4.2.0', 'scikit-learn>=0.24.1'],
    platforms=["any"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires='>=3.6',
)
