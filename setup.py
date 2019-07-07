#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Setup for dyndnsc."""

import os
import re
import sys
from setuptools import setup
from setuptools import __version__ as setuptools_version

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
    "Intended Audience :: System Administrators",
    "License :: DFSG approved",
    "License :: OSI Approved",
    "License :: OSI Approved :: MIT License",
    "Topic :: Internet",
    "Topic :: Internet :: Name Service (DNS)",
    "Topic :: Software Development :: Libraries :: Python Modules",
    "Topic :: System :: Systems Administration",
    "Environment :: Console",
    "Natural Language :: English",
    "Operating System :: MacOS :: MacOS X",
    "Operating System :: POSIX :: Linux",
    "Operating System :: POSIX :: BSD",
    "Programming Language :: Python",
    "Programming Language :: Python :: 2.7",
    "Programming Language :: Python :: 3.4",
    "Programming Language :: Python :: 3.5",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7"
)

INSTALL_REQUIRES = [
    "daemonocle>=1.0.1",
    "dnspython>=1.15.0",
    "netifaces>=0.10.5",
    "requests>=2.0.1",
    "setuptools",
]

TESTS_REQUIRE = [
    "mock; python_version < '3.0'",  # pep508 syntax may not work on older toolchains
    "bottle==0.12.13",
    "pytest>=3.2.5,<5.0.0"
]

EXTRAS_REQUIRE = {}

# See https://hynek.me/articles/conditional-python-dependencies/
# for a good explanation of this hackery.
if int(setuptools_version.split(".", 1)[0]) < 18:
    # For legacy setuptools + sdist
    assert "bdist_wheel" not in sys.argv, "setuptools 18 required for wheels."  # noqa: S101
    if sys.version_info[0:2] < (3, 0):
        INSTALL_REQUIRES.append("IPy>=0.56")
        INSTALL_REQUIRES.append("argparse")
        INSTALL_REQUIRES.append("pyOpenSSL")
        INSTALL_REQUIRES.append("ndg-httpsclient")
        INSTALL_REQUIRES.append("pyasn1")
else:
    EXTRAS_REQUIRE[":python_version<'3.0'"] = [
        "IPy>=0.56",
        "argparse",
        # This is equivalent to requests[security] which exists since
        # requests 2.4.1 It is required in older Pythons that do not
        # understand SNI certificates. When these libraries are available
        # they are being used and incidentally also support SNI
        "pyOpenSSL",
        "ndg-httpsclient",
        "pyasn1",
    ]

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
    # https://packaging.python.org/tutorials/distributing-packages/#python-requires
    python_requires=">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*",
    setup_requires=["pytest-runner"],
    install_requires=INSTALL_REQUIRES,
    extras_require=EXTRAS_REQUIRE,
    entry_points={
        "console_scripts": [
            "dyndnsc=dyndnsc.cli:main",
        ],
    },
    classifiers=CLASSIFIERS,
    test_suite="dyndnsc.tests",
    tests_require=TESTS_REQUIRE,
    package_data={"dyndnsc/resources": ["dyndnsc/resources/*.ini"]},
    include_package_data=True,
    zip_safe=False
)
