.. _quickstart:

Quickstart
==========


Eager to get started? This page gives a good introduction in how to get started
with Dyndnsc. This assumes you already have Dyndnsc installed. If you do not,
head over to the :ref:`Installation <install>` section.

First, make sure that:

* Dyndnsc is :ref:`installed <install>`
* Dyndnsc is :ref:`up-to-date <updates>`


Let's get started with some simple examples.


Examples
--------

Basic example that should fit most peoples needs:

.. code-block:: bash

    $ dyndnsc  --hostname test.dyndns.com --userid bob --password=fub4r


Are you using `Miredo <http://www.remlab.net/miredo/>`_ and want to assign
a hostname dynamically to your ipv6 tunnel?

.. code-block:: bash

    $ dyndnsc  --hostname test.dyndns.com --userid bob --method=teredo

Passing parameters for IP detection
-----------------------------------


Custom services
---------------


Error handling
--------------
