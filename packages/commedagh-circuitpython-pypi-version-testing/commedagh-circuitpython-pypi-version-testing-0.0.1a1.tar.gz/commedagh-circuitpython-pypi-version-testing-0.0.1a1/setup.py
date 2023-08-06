# SPDX-FileCopyrightText: 2017 Scott Shawcroft, written for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2021 James Carr for Commedagh
#
# SPDX-License-Identifier: MIT

"""A setuptools based setup module.

See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

from setuptools import setup, find_packages
import subprocess

# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))


def get_version_from_git():
    try:
        git_out = subprocess.check_output(["git", "describe", "--tags"])
        version = git_out.strip().decode("utf-8")

        # Detect a development build and mutate it to be valid semver and valid python version.
        pieces = version.split("-")
        if len(pieces) > 2:
            # Merge the commit portion onto the commit count since the tag.
            pieces[-2] += "+" + pieces[-1]
            pieces.pop()
            # Merge the commit count and build to the pre-release identifier.
            pieces[-2] += ".dev." + pieces[-1]
            pieces.pop()
        version = "-".join(pieces)
        return version
    except subprocess.CalledProcessError as cpe:
        # Can't figure a version most likely because there are no tags yet
        return "0.0.0"


# Get the long description from the README file
with open(path.join(here, "README.rst"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    # Community Bundle Information
    name="commedagh-circuitpython-pypi-version-testing",
    # use_scm_version=True,
    # setup_requires=["setuptools_scm"],
    description="testing pypi versioning",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    # The project's main homepage.
    url="https://github.com/lesamouraipourpre/Commedagh_CircuitPython_pypi-version-testing.git",
    # Author details
    author="James Carr",
    author_email="",
    version=get_version_from_git(),
    install_requires=[
        "Adafruit-Blinka",
        "n",
    ],
    # Choose your license
    license="MIT",
    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries",
        "Topic :: System :: Hardware",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
    ],
    # What does your project relate to?
    keywords="adafruit blinka circuitpython micropython pypi-version-testing test pypi "
    "version",
    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    # TODO: IF LIBRARY FILES ARE A PACKAGE FOLDER,
    #       CHANGE `py_modules=['...']` TO `packages=['...']`
    py_modules=["commedagh_pypi-version-testing"],
)
