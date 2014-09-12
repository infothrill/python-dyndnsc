#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import re
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

v = open(os.path.join(os.path.dirname(__file__), 'dyndnsc', '__init__.py'))
VERSION = re.compile(r".*__version__ = '(.*?)'", re.S).match(v.read()).group(1)
v.close()

CLASSIFIERS = (
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'License :: DFSG approved',
    'License :: OSI Approved',
    'License :: OSI Approved :: MIT License',
    'Topic :: Internet :: Name Service (DNS)',
    'Topic :: Software Development :: Libraries :: Python Modules',
    'Environment :: Console',
    'Natural Language :: English',
    'Operating System :: MacOS :: MacOS X',
    'Operating System :: POSIX :: Linux',
    'Operating System :: POSIX :: BSD :: FreeBSD',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2.6',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3.2',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4'
)


def patch_test_requires(requires):
    """python version compatibility"""
    if sys.version_info < (3, 3):
        return requires + ["mock"]
    else:
        return requires


def patch_install_requires(requires):
    """python version compatibility"""
    to_add = []
    if sys.version_info < (3, 3):
        to_add.append("IPy>=0.56")
    if sys.version_info < (3, 2):
        to_add.append("argparse")
        # This is equivalent to requests[security] which exists since
        # requests 2.4.1 It is required in older Pythons that do not
        # understand SNI certificates. When these libraries are available
        # they are being used and incidently also support SNI
        to_add.append("pyOpenSSL")
        to_add.append("ndg-httpsclient")
        to_add.append("pyasn1")
    to_add.append("netifaces>=0.10.4")  # hm, this still breaks on some builds
    if sys.version_info < (2, 7):  # continue support for python 2.6
        to_add.append("importlib")
    return requires + to_add

if sys.version_info >= (3, 0):
    pass
else:
    # work around python issue http://bugs.python.org/issue15881
    # affects only python2 when using multiprocessing and if nose is installed
    import multiprocessing

setup(
    name='dyndnsc',
    packages=[
        'dyndnsc',
        'dyndnsc.common',
        'dyndnsc.detector',
        'dyndnsc.plugins',
        'dyndnsc.tests',
        'dyndnsc.updater',
    ],
    version=VERSION,
    author='Paul Kremer',
    author_email='@'.join(("paul", "spurious.biz")),  # avoid spam,
    license='MIT License',
    description='dynamic dns (dyndns) update client that tries to be '
                'extensible, re-usable and efficient on network resources',
    long_description=(open('README.rst', 'r').read() + '\n\n' +
                      open('CHANGELOG.rst', 'r').read()),
    url='https://github.com/infothrill/python-dyndnsc',
    install_requires=patch_install_requires(['requests']),
    entry_points=("""
        [console_scripts]
        dyndnsc=dyndnsc.cli:main
    """),
    classifiers=CLASSIFIERS,
    test_suite='dyndnsc.tests',
    tests_require=patch_test_requires(['bottle==0.12.7'])
)
