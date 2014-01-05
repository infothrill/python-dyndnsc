.. _install:

Installation
============

This part of the documentation covers the installation of Dyndnsc.
The first step to using any software package is getting it properly installed.


Pip
---

Installing Dyndnsc is simple with `pip <http://www.pip-installer.org/>`_::

    $ pip install dyndnsc

If using python2 and pip >= 1.5, more arguments are required::

    $ pip install dyndnsc --allow-external netifaces --allow-unverified netifaces


Cheeseshop (PyPI) Mirror
------------------------

If the Cheeseshop (a.k.a. PyPI) is down, you can also install Dyndnsc from one
of the mirrors. `Crate.io <http://crate.io>`_ is one of them::

    $ pip install -i http://simple.crate.io/ dyndnsc


Get the Code
------------

Dyndnsc is actively developed on GitHub, where the code is
`always available <https://github.com/infothrill/python-dyndnsc>`_.

You can either clone the public repository::

    git clone git://github.com/infothrill/python-dyndnsc.git

Download the `tarball <https://github.com/infothrill/python-dyndnsc/tarball/master>`_::

    $ curl -OL https://github.com/infothrill/python-dyndnsc/tarball/master

Or, download the `zipball <https://github.com/infothrill/python-dyndnsc/zipball/master>`_::

    $ curl -OL https://github.com/infothrill/python-dyndnsc/zipball/master


Once you have a copy of the source, you can embed it in your Python package,
or install it into your site-packages easily::

    $ python setup.py install
