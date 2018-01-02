#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Setup for dyndnsc."""

import os
import re
import sys
from setuptools import setup

BASEDIR = os.path.dirname(__file__)

with open(os.path.join(BASEDIR, "dyndnsc", "__init__.py"), "r") as f:
    PACKAGE_INIT = f.read()

VERSION = re.compile(
    r".*__version__ = \"(.*?)\"", re.S).match(PACKAGE_INIT).group(1)

with open(os.path.join(BASEDIR, "README.rst"), "r") as f:
    README = f.read()

with open(os.path.join(BASEDIR, "CHANGELOG.rst"), "r") as f:
    CHANGELOG = f.read()


CLASSIFIERS = (
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "License :: DFSG approved",
    "License :: OSI Approved",
    "License :: OSI Approved :: MIT License",
    "Topic :: Internet :: Name Service (DNS)",
    "Topic :: Software Development :: Libraries :: Python Modules",
    "Environment :: Console",
    "Natural Language :: English",
    "Operating System :: MacOS :: MacOS X",
    "Operating System :: POSIX :: Linux",
    "Operating System :: POSIX :: BSD :: FreeBSD",
    "Programming Language :: Python",
    "Programming Language :: Python :: 2.7",
    "Programming Language :: Python :: 3.4",
    "Programming Language :: Python :: 3.5",
    "Programming Language :: Python :: 3.6"
)


def patch_test_requires(requires):
    """Ensure python version compatibility."""
    to_add = []
    if sys.version_info < (3, 0):
        to_add.append("mock")  # needed for py27
    return requires + to_add


def patch_install_requires(requires):
    """Ensure python version compatibility."""
    to_add = []
    if sys.version_info < (3, 0):
        to_add.append("IPy>=0.56")
        to_add.append("argparse")
        # This is equivalent to requests[security] which exists since
        # requests 2.4.1 It is required in older Pythons that do not
        # understand SNI certificates. When these libraries are available
        # they are being used and incidentally also support SNI
        to_add.append("pyOpenSSL")
        to_add.append("ndg-httpsclient")
        to_add.append("pyasn1")
    return requires + to_add


setup(
    name="dyndnsc",
    packages=[
        "dyndnsc",
        "dyndnsc.common",
        "dyndnsc.detector",
        "dyndnsc.plugins",
        "dyndnsc.resources",
        "dyndnsc.tests",
        "dyndnsc.updater",
    ],
    version=VERSION,
    author="Paul Kremer",
    author_email="@".join(("paul", "spurious.biz")),  # avoid spam,
    license="MIT License",
    description="dynamic dns (dyndns) update client with support for multiple "
                "protocols",
    long_description=README + "\n\n" + CHANGELOG,
    keywords="dynamic dns dyndns",
    url="https://github.com/infothrill/python-dyndnsc",
    setup_requires=["pytest-runner"],
    install_requires=patch_install_requires(
        ["requests>=2.0.1", "setuptools", "netifaces>=0.10.5", "daemonocle>=1.0.1"]),
    entry_points=("""
        [console_scripts]
        dyndnsc=dyndnsc.cli:main
    """),
    classifiers=CLASSIFIERS,
    test_suite="dyndnsc.tests",
    tests_require=patch_test_requires([
        "bottle==0.12.7",
        "pep8>=1.3",
        "pytest>=3.2.5"
    ]),
    package_data={"dyndnsc/resources": ["dyndnsc/resources/*.ini"]},
    include_package_data=True,
    zip_safe=False
)
