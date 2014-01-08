Dyndnsc - dynamic dns update client
===================================

.. image:: https://travis-ci.org/infothrill/python-dyndnsc.png
    :target: https://travis-ci.org/infothrill/python-dyndnsc

.. image:: https://coveralls.io/repos/infothrill/python-dyndnsc/badge.png
        :target: https://coveralls.io/r/infothrill/python-dyndnsc

.. image:: https://badge.fury.io/py/dyndnsc.png
    :target: http://badge.fury.io/py/dyndnsc


*dyndnsc* is both a script to be used directly as well as a re-usable and
hopefully extensible python package for doing updates over http to dynamic
dns services. This package currently focuses on supporting http based update
protocols.



Examples
========

Basic example that should fit most peoples needs:

.. code-block:: bash

    $ dyndnsc --updater-dyndnsv2-hostname test.dyndns.com \ 
        --updater-dyndnsv2-userid bob \
        --updater-dyndnsv2-password=xxxxxxxx


Are you using `Miredo <http://www.remlab.net/miredo/>`_ and want to assign
a hostname dynamically to your ipv6 tunnel?

.. code-block:: bash

    $ dyndnsc --updater-dyndnsv2-hostname test.dyndns.com \ 
        --updater-dyndnsv2-userid bob \
        --updater-dyndnsv2-password=xxxxxxxx \
        --method teredo


Updating an IPv4 record on nsupdate.info with web based ip autodetection:

.. code-block:: bash

    $ dyndnsc --updater-nsupdate \
              --updater-nsupdate-hostname test.nsupdate.info \
              --updater-nsupdate-userid   test.nsupdate.info \
              --updater-nsupdate-password xxxxxxxx \
              --loop --sleeptime 300 \
              --method=webcheck

Updating an IPv6 record on nsupdate.info with interface based ip detection:

.. code-block:: bash

    $ dyndnsc --updater-nsupdate \
              --updater-nsupdate-hostname test.nsupdate.info \
              --updater-nsupdate-userid test.nsupdate.info \
              --updater-nsupdate-password xxxxxxxx \
              --loop --sleeptime 300 \
              --method=Iface,netmask:2001:470:1234:5678::/64,iface:eth0,family:INET6


Compatible protocols
====================
* `dnsimple <http://developer.dnsimple.com/>`_
* `dyndns2 <http://dyn.com/support/developers/api/>`_
* `freedns.afraid.org <http://freedns.afraid.org/>`_

Feel free to send pull requests to add more.

Compatible services
===================
This list is incomplete, since there are a lot of dyndns2 compatible services
out there.

* `dnsimple.com <http://dnsimple.com/>`_ (protocol: dnsimple)
* `dyn.com <http://dyn.com/>`_ (protocol: dyndnsv2)
* `freedns.afraid.org <http://freedns.afraid.org/>`_ (protocol: afraid)
* `hopper.pw <https://www.hopper.pw/>`_ (protocol: dyndnsv2)
* `no-ip <https://www.no-ip.com/>`_ (protocol: dyndnsv2)
* `nsupdate.info <https://nsupdate.info/>`_ (protocol: dyndnsv2)

To specify a dyndnsv2 compatible service on the command line, add the -service_url argument:

.. code-block:: bash

    $ dyndnsc --updater-dyndnsv2-hostname test.dyndns.com \ 
        --updater-dyndnsv2-userid bob \
        --updater-dyndnsv2-password=xxxxxxxx \
        --updater-dyndnsv2-service_url=https://otherservice.example.com/nic/update

Installation
============

.. code-block:: bash

    $ pip install dyndnsc

or, if you want to work using the source tarball:

.. code-block:: bash

    $ python setup.py install
  

Requirements
============
* Python 2.6, 2.7, 3.2 or 3.3+


Documentation
=============

Documentation is available at http://dyndnsc.readthedocs.org/.
  
Status
======
*dyndnsc* is currently still in alpha stage, which means that any interface can
still change at any time. For this to change, it shall be sufficient to have
documented use of this package which will necessitate stability (i.e.
community process).
