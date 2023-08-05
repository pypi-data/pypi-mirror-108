import setuptools
from configparser import ConfigParser

with open ("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name = "uqpylab",
    version = "0.02",
    author = "C. Lataniotis, S. Marelli, B. Sudret",
    author_email = "contact@uq-cloud.io",
    description = "Uncertainty quantification in python based on UQLab.",
    long_description = long_description,
    long_description_content_type="text/markdown",
    url="https://uq-cloud.io",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    include_package_data=True,
    install_requires=[
          'scipy','numpy','matplotlib'
      ]
)
