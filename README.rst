Dyndnsc - dynamic dns update client
===================================

.. image:: https://img.shields.io/pypi/v/dyndnsc.svg
    :target: https://pypi.python.org/pypi/dyndnsc

.. image:: https://img.shields.io/pypi/l/dyndnsc.svg
    :target: https://pypi.python.org/pypi/dyndnsc

.. image:: https://img.shields.io/pypi/pyversions/dyndnsc.svg
    :target: https://pypi.python.org/pypi/dyndnsc

.. image:: https://travis-ci.org/infothrill/python-dyndnsc.svg?branch=master
    :target: https://travis-ci.org/infothrill/python-dyndnsc

.. image:: https://img.shields.io/coveralls/infothrill/python-dyndnsc/master.svg
    :target: https://coveralls.io/r/infothrill/python-dyndnsc?branch=master
    :alt: Code coverage

*Dyndnsc* is a command line client for sending updates to dynamic
dns (ddns, dyndns) services. It supports multiple protocols and services,
and it has native support for ipv6. The configuration file allows
using foreign, but compatible services. *Dyndnsc* ships many different IP
detection mechanisms, support for configuring multiple services in one place
and it has a daemon mode for running unattended. It has a plugin system
to provide external notification services.


Quickstart / Documentation
==========================
See the Quickstart section of the https://dyndnsc.readthedocs.io/


Installation
============

.. code-block:: bash

    # from pypi:
    pip install dyndnsc

    # using docker:
    docker pull infothrill/dyndnsc-x86-alpine

    # from downloaded source:
    python setup.py install

    # directly from github:
    pip install https://github.com/infothrill/python-dyndnsc/zipball/develop


Requirements
============
* Python 2.7 or 3.4+


Status
======
*Dyndnsc* is still in alpha stage, which means that any interface can still
change at any time. For this to change, it shall be sufficient to have
documented use of this package which will necessitate stability (i.e.
community process).
