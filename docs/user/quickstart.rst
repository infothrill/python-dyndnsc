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

A basic example that should fit most peoples needs using the dyndns.com service:

.. code-block:: bash

    $ dyndnsc --updater-dyndns2 \
              --updater-dyndns2-hostname=test.dyndns.com \
              --updater-dyndns2-userid=bob \
              --updater-dyndns2-password=fub4r

Updating an IPv6 address when using `Miredo <http://www.remlab.net/miredo/>`_:

.. code-block:: bash

    $ dyndnsc --updater-nsupdate \
              --updater-nsupdate-hostname test.nsupdate.info \
              --updater-nsupdate-userid   test.nsupdate.info \
              --updater-nsupdate-password xxxxxxxx \
              --detector teredo \
              --dns dns,family:INET6

Updating an IPv4 record on nsupdate.info with web based ip autodetection:

.. code-block:: bash

    $ dyndnsc --updater-nsupdate \
              --updater-nsupdate-hostname test.nsupdate.info \
              --updater-nsupdate-userid   test.nsupdate.info \
              --updater-nsupdate-password xxxxxxxx \
              --detector webcheck4,url:http://ipv4.nsupdate.info/myip,parser:plain \
              --dns dns,family:INET

Updating an IPv6 record on nsupdate.info with interface based ip detection:

.. code-block:: bash

    $ dyndnsc --updater-nsupdate \
              --updater-nsupdate-hostname test.nsupdate.info \
              --updater-nsupdate-userid test.nsupdate.info \
              --updater-nsupdate-password xxxxxxxx \
              --detector Iface,netmask:2001:470:1234:5678::/64,iface:eth0,family:INET6 \
              --dns dns,family:INET6


Passing parameters for IP detection
-----------------------------------

Currently, detectors can receive additional command line arguments by
specifying them using comma/colon separated arguments:

.. code-block:: bash

    $ dyndnsc --detector iface,iface:en0,family:INET
    $ dyndnsc --detector webcheck4,url:http://ipv4.nsupdate.info/myip,parser:plain

This is a bit unflexible an might be changed in future versions.

Custom services
---------------

If you are using a dyndns2 compatible service and need to specify the update
URL explicitly, you can add the argument --updater-dyndns2-service_url:

.. code-block:: bash

    $ dyndnsc --updater-dyndns2 --updater-dyndns2-hostname=test.dyndns.com --updater-dyndns2-userid=bob --updater-dyndns2-password=fub4r --updater-dyndns2-service_url=https://dyndns.example.com/nic/update


Error handling
--------------

Connection errors and timeout errors on the socket level and http level are
mostly handled as transient and simply ignored, i.e. updating and/or detecting
an IP will fail with a log message but the client should remain active and
retry later.

Some errors are not handled gracefully, for example if there is an SSL handshake
issue when using a https connection, dyndnsc will typically fail.

Thus, depending on your needs, it might be required to put the dyndnsc client
inside a retry loop to run it in a completely unattended way. Don't
be fooled by the --daemon option, it is available, but the design of the
dyndnsc program does not provide longevity guarantuees. Feel free to contribute
some by sending pull requests!

