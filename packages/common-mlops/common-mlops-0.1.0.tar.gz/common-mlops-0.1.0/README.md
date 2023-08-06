# common-mlops

This is a set of utilities for end-to-end lifecycle of Machine Learning applications in Python for Inria-Chile.
Could be used like a framework and tooling for rapid development of data science and MLOps functions.

Here’s the folder structure for the repository:

```
common-mlops/
|
├── data/
│   ├── prepared/
│   └── raw/
│   └── metrics/
├── model/
├── mlops/
|   └── *.py
├── test/
|   └── test_*.py
├── venv/
├── check_credentials.sh
├── install.sh
├── LICENSE
├── README.md
├── requirements.txt
├── s3*.py
└── setup.py
```

There are the folloging folders in our repository:

- data/ is all versions of the dataset.
- data/raw/ is the data obtained from an external source.
- data/prepared/ is for data modified internally.
- data/metrics/ is for tracking the performance metrics of our models.
- model/ is for machine learning models.
- mlops/ is the source code. Python classes used by the Python scripts.
- test/ is the pyunit of source code.
- venv/ is the virtual environment.
- check_credentials.sh bash for check the AWS credentials.
- install.sh bash for check the installation.
- LICENSE
- requirements.txt the dependencies.
- s3*.py Python scripts for bash executions.
- setup.py the configuration of the package.

# Installation Linux

Perform the following steps in order to install this program. Replace 'access_key_id' and 'secret_access_key' by the account AWS Credentials associated to poc-inriacl.

```sh
git clone https://gitlab.com/Inria-Chile/common-mlops.git
./common-mlops/install.sh access_key_id secret_access_key
pip3 uninstall common-mlops
# Version of test
pip3 install -i https://test.pypi.org/simple/ common-mlops
# Version of production
pip3 install common-mlops
```

# Updates in test.pypi.org

Perform the following steps in order to publish new versions to test.pypi.org:

```sh
sudo rm -rf build common_mlops.egg-info dist
bumpversion --current-version 1.0.0 minor setup.py mlops/__init__.py
python3 setup.py sdist bdist_wheel
# Version of test
twine check dist/*
twine upload --repository-url https://test.pypi.org/legacy/ dist/*
# Version of production
twine upload dist/*
```

# Tests

Run the unit tests:

```sh
python3 -m unittest
```

# Usage

See the example of usage in:

- https://gitlab.com/Inria-Chile/oceania/data-read
- http://twiki.inriadev.cl/twiki/bin/view/Sandbox/OceaniaClassDiagramPOCS3DVC

# Docker

Build the image:

```sh
docker build -t common-mlops .
```

```sh
docker pull common-mlops
```

Run the image:

```sh
docker run -v$HOME/.aws:/root/.aws:ro -e S3_ACCESS_KEY_ID=access_key_id -e S3_SECRET_ACCESS_KEY=secret_access_key -e AWS_ACCESS_KEY_ID=access_key_id -e AWS_SECRET_ACCESS_KEY=secret_access_key common-mlops .
```

# References

- https://test.pypi.org/project/common-mlops
- https://pypi.org/project/common-mlops
- https://anno-ai.medium.com/mlops-and-data-managing-large-ml-datasets-with-dvc-and-s3-part-1-d5b8f2fb8280
- https://martinfowler.com/articles/cd4ml.html
- https://christophergs.com/machine%20learning/2020/03/14/how-to-monitor-machine-learning-models/
