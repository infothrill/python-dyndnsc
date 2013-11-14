#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

classifiers = [line.strip() for line in """
Development Status :: 3 - Alpha
Intended Audience :: Developers
License :: DFSG approved
License :: OSI Approved
License :: OSI Approved :: MIT License
Topic :: Internet :: Name Service (DNS)
Topic :: Software Development :: Libraries :: Python Modules
Environment :: Console
Natural Language :: English
Operating System :: MacOS :: MacOS X
Operating System :: POSIX :: Linux
Operating System :: POSIX :: BSD :: FreeBSD
Programming Language :: Python
Programming Language :: Python :: 2.6
Programming Language :: Python :: 2.7
Programming Language :: Python :: 3.2
Programming Language :: Python :: 3.3
""".splitlines() if len(line) > 0]

install_requires = ["requests", "IPy>=0.56"]
if sys.version_info >= (3, 0):
    install_requires.append("netifaces-py3==0.8")
else:
    install_requires.append("netifaces>=0.4")
    # work around python issue http://bugs.python.org/issue15881
    # affects only python2 when using multiprocessing and if nose is installed
    import multiprocessing

if sys.version_info < (3, 2):
    install_requires.append("argparse")
if sys.version_info < (2, 7):  # continue support for python 2.6
    install_requires.append("importlib")

setup(name="dyndnsc",
      packages=["dyndnsc", "dyndnsc.common", "dyndnsc.detector",
                "dyndnsc.updater", "dyndnsc.tests"],
      version="0.3.2",
      author="Paul Kremer",
      author_email="@".join(("paul", "spurious.biz")),  # avoid spam,
      license="MIT License",
      description="dynamic dns update client package that tries to be "
            "extensible, re-usable and efficient on network resources",
      long_description=(open("README.rst", "r").read() + "\n\n" +
                        open("CHANGELOG.rst", "r").read()),
      url="https://github.com/infothrill/python-dyndnsc",
      install_requires=install_requires,
      entry_points=("""
                      [console_scripts]
                      dyndnsc=dyndnsc.cli:main
                      """),
      classifiers=classifiers,
      test_suite='dyndnsc.tests',
      tests_require=['bottle==0.11.6'],
      )
