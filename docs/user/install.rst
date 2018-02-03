.. _install:

Installation
============

This part of the documentation covers the installation of Dyndnsc.
The first step to using any software package is getting it properly installed.


Pip / pipsi
-----------

Installing Dyndnsc is simple with `pip <http://www.pip-installer.org/>`_::

    pip install dyndnsc

Or, if you prefer a more encapsulated way, use `pipsi <https://github.com/mitsuhiko/pipsi/>`_::

    pipsi install dyndnsc


Docker
------

`Docker <https://www.docker.com>`_ images are provided for the following architectures.

x86::

    docker pull infothrill/dyndnsc-x86-alpine

See also https://hub.docker.com/r/infothrill/dyndnsc-x86-alpine/

armhf::

    docker pull infothrill/dyndnsc-armhf-alpine

See also https://hub.docker.com/r/infothrill/dyndnsc-armhf-alpine/

Get the Code
------------

Dyndnsc is developed on GitHub, where the code is
`available <https://github.com/infothrill/python-dyndnsc>`_.

You can clone the public repository::

    git clone https://github.com/infothrill/python-dyndnsc.git

Once you have a copy of the source, you can embed it in your Python package,
or install it into your site-packages easily::

    python setup.py install
