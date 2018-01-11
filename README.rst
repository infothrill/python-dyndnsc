[![FOSSA Status](https://app.fossa.io/api/projects/git%2Bgithub.com%2Finfothrill%2Fpython-dyndnsc.svg?type=shield)](https://app.fossa.io/projects/git%2Bgithub.com%2Finfothrill%2Fpython-dyndnsc?ref=badge_shield)

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

.. image:: https://img.shields.io/requires/github/infothrill/python-dyndnsc.svg
    :target: https://requires.io/github/infothrill/python-dyndnsc/requirements/?branch=master
    :alt: Requirements Status

*Dyndnsc* is a command line client for sending updates to dynamic
dns (ddns, dyndns) services. It supports multiple protocols and services,
and it is compatible with ipv4 as well as ipv6. The configuration file allows
using foreign, but compatible services. *Dyndnsc* ships many different IP
detection mechanisms, support for configuring multiple services in one place
and it has a daemon mode for running unattended. It has a plugin architecture
for supporting notification services like Growl or OS X Notification center.


Quickstart / Documentation
==========================
See the Quickstart section of the http://dyndnsc.readthedocs.org/


Installation
============

.. code-block:: bash

    $ # from pypi:
    $ pip install dyndnsc

    $ # from downloaded source:
    $ python setup.py install

    $ # directly from github:
    $ pip install https://github.com/infothrill/python-dyndnsc/zipball/develop


Requirements
============
* Python 2.7 or 3.4+


Status
======
*Dyndnsc* is currently still in alpha stage, which means that any interface can
still change at any time. For this to change, it shall be sufficient to have
documented use of this package which will necessitate stability (i.e.
community process).


## License
[![FOSSA Status](https://app.fossa.io/api/projects/git%2Bgithub.com%2Finfothrill%2Fpython-dyndnsc.svg?type=large)](https://app.fossa.io/projects/git%2Bgithub.com%2Finfothrill%2Fpython-dyndnsc?ref=badge_large)