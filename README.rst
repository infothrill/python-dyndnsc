Dyndnsc - dynamic dns update client
===================================

.. image:: https://travis-ci.org/infothrill/python-dyndnsc.png
    :target: https://travis-ci.org/infothrill/python-dyndnsc

.. image:: https://coveralls.io/repos/infothrill/python-dyndnsc/badge.png
        :target: https://coveralls.io/r/infothrill/python-dyndnsc

.. image:: https://badge.fury.io/py/dyndnsc.png
    :target: http://badge.fury.io/py/dyndnsc

.. image:: https://pypip.in/d/dyndnsc/badge.png
        :target: https://crate.io/packages/dyndnsc/


*dyndnsc* is both a script to be used directly as well as a re-usable and
hopefully extensible python package for doing updates over http to dynamic
dns services. This package currently focuses on supporting the dyndns2 protocol
(http://dyn.com/support/developers/api/) and variations thereof.



Examples
========

Basic example that should fit most peoples needs:

.. code-block:: bash

    $ dyndnsc  --hostname test.dyndns.com --userid bob --password=fub4r


Are you using `Miredo <http://www.remlab.net/miredo/>`_ and want to assign
a hostname dynamically to your ipv6 tunnel?

.. code-block:: bash

    $ dyndnsc  --hostname test.dyndns.com --userid bob
           --method=Iface,netmask:2001:0000::/32,iface:tun0,family:INET6


Supported services
==================
Currently, (at least basic) support is offered for

* `dyndns.org <http://dyndns.org/>`_
* `no-ip <https://www.no-ip.com/>`_
* `dnsupdate.info <https://dnsupdate.info/>`_

Feel free to send pull requests to add more.

Installation
============

.. code-block:: bash

    $ pip install dyndnsc

or, if you want to work using the source tarball:

.. code-block:: bash

    $ python setup.py install
  

Requirements
============
* Python 2.6, 2.7, 3.2 or 3.3


Goals
=====
*dyndnsc* was born as a minimal module for use in the *ANGEL APP*, a p2p
filesystem on top of webdav. At the time, the command line interface was not
important. Now that time has passed, the goals are essentially to provide
both an easy to use command line tool as well as providing an OK API for
developers who want to add dyndns capabilities to their software. Also,
providing support for many different ways of detecting and updating IP/DNS
records is important.
  
Status
======
*dyndnsc* is currently still in alpha stage, which means that any interface can
still change at any time. For this to change, it shall be sufficient to have
documented use of this package which will necessitate stability (i.e.
community process).
