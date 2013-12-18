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

    $ dyndnsc  --hostname test.dyndns.com --userid bob --password=fub4r


Are you using `Miredo <http://www.remlab.net/miredo/>`_ and want to assign
a hostname dynamically to your ipv6 tunnel?

.. code-block:: bash

    $ dyndnsc  --hostname test.dyndns.com --userid bob --method=teredo


Supported protocols
===================
* `dyndns2 <http://dyn.com/support/developers/api/>`_
* `freedns.afraid.org <http://freedns.afraid.org/>`_

Feel free to send pull requests to add more.

Supported services
==================
This list is incomplete, since every supported protocol can potentially be used
with a different service/URL. Work is in progress to decouple protocols from
services.

* `dyn.com <http://dyn.com/>`_
* `freedns.afraid.org <http://freedns.afraid.org/>`_
* `no-ip <https://www.no-ip.com/>`_
* `nsupdate.info <https://nsupdate.info/>`_

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
