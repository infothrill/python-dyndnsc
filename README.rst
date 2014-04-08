Dyndnsc - dynamic dns update client
===================================

.. image:: https://travis-ci.org/infothrill/python-dyndnsc.svg?branch=develop
    :target: https://travis-ci.org/infothrill/python-dyndnsc

.. image:: https://pypip.in/d/dyndnsc/badge.png
    :target: https://pypi.python.org/pypi/dyndnsc

.. image:: https://coveralls.io/repos/infothrill/python-dyndnsc/badge.png
    :target: https://coveralls.io/r/infothrill/python-dyndnsc

.. image:: https://badge.fury.io/py/dyndnsc.png
    :target: http://badge.fury.io/py/dyndnsc

.. image:: https://requires.io/github/infothrill/python-dyndnsc/requirements.png?branch=develop
   :target: https://requires.io/github/infothrill/python-dyndnsc/requirements/?branch=develop
   :alt: Requirements Status

*dyndnsc* is both a script to be used directly as well as a re-usable and
hopefully extensible python package for doing updates over http to dynamic
dns services. This package currently focuses on supporting http based update
protocols.



Examples
========
See the Quickstart section of the http://dyndnsc.readthedocs.org/

Compatible protocols
====================
* `dnsimple <http://developer.dnsimple.com/>`_
* `dyndns2 <http://dyn.com/support/developers/api/>`_
* `freedns.afraid.org <http://freedns.afraid.org/>`_

Feel free to send pull requests to add more.

Compatible services
===================
This list is incomplete, since there are a lot of compatible services
out there. Some of these services offer free accounts, some are paid or
subscription based. Either way, this list should probably go elsewhere...

* `dns.he.net <https://dns.he.net/>`_ (protocol: dyndns2)
* `dnsdynamic.org <http://www.dnsdynamic.org/>`_ (protocol: dyndns2)
* `dnsimple.com <http://dnsimple.com/>`_ (protocol: dnsimple)
* `dyn.com <http://dyn.com/>`_ (protocol: dyndns2)
* `freedns.afraid.org <http://freedns.afraid.org/>`_ (protocol: afraid)
* `hopper.pw <https://www.hopper.pw/>`_ (protocol: dyndns2)
* `no-ip <https://www.no-ip.com/>`_ (protocol: dyndns2)
* `nsupdate.info <https://nsupdate.info/>`_ (protocol: dyndns2)

To specify a dyndns2 compatible service on the command line, add the -service_url argument:

.. code-block:: bash

    $ dyndnsc --updater-dyndns2 \
        --updater-dyndns2-hostname test.dyndns.com \ 
        --updater-dyndns2-userid bob \
        --updater-dyndns2-password=xxxxxxxx \
        --updater-dyndns2-service_url=https://otherservice.example.com/nic/update

Installation
============

.. code-block:: bash

    $ pip install dyndnsc

or, if you want to work using the source tarball:

.. code-block:: bash

    $ python setup.py install
  

Requirements
============
* Python 2.6, 2.7 or 3.2+


Documentation
=============

Documentation is available at http://dyndnsc.readthedocs.org/.
  
Status
======
*dyndnsc* is currently still in alpha stage, which means that any interface can
still change at any time. For this to change, it shall be sufficient to have
documented use of this package which will necessitate stability (i.e.
community process).
