import pathlib
from setuptools import setup
import setuptools

# The directory containing this file
HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

setup(
name = "moorkh",
version = "0.0.2",
author = "Akshay Gupta",
author_email = "akshay.bis2000@gmail.com",
description = "Buddhu is a Adversarial examples generation library",
long_description = README,
long_description_content_type = "text/markdown",
url = "https://github.com/akshay-gupta123/moorkh",
packages = setuptools.find_packages(),
project_urls = {"Bug Tracker" : "https://github.com/akshay-gupta123/moorkh/issues"},
classifiers = ["Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License"],
python_requires = '>=3.6' 
)