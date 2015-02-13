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


Command line usage
------------------

A basic example that should fit most peoples needs using the dyndns.com service:

.. code-block:: bash

    $ dyndnsc --updater-dyndns2 \
              --updater-dyndns2-hostname=test.dyndns.com \
              --updater-dyndns2-userid=bob \
              --updater-dyndns2-password=fub4r

Updating an IPv6 address when using `Miredo <http://www.remlab.net/miredo/>`_:

.. code-block:: bash

    $ dyndnsc --updater-dyndns2 \
              --updater-dyndns2-hostname test.nsupdate.info \
              --updater-dyndns2-userid   test.nsupdate.info \
              --updater-dyndns2-password xxxxxxxx \
              --detector teredo

Updating an IPv4 record on nsupdate.info with web based ip autodetection:

.. code-block:: bash

    $ dyndnsc --updater-dyndns2 \
              --updater-dyndns2-hostname test.nsupdate.info \
              --updater-dyndns2-userid   test.nsupdate.info \
              --updater-dyndns2-password xxxxxxxx \
              --updater-dyndns2-url=https://nsupdate.info/nic/update \
              --detector webcheck4,url:http://ipv4.nsupdate.info/myip,parser:plain

Updating an IPv6 record on nsupdate.info with interface based ip detection:

.. code-block:: bash

    $ dyndnsc --updater-dyndns2 \
              --updater-dyndns2-hostname test.nsupdate.info \
              --updater-dyndns2-userid test.nsupdate.info \
              --updater-dyndns2-password xxxxxxxx \
              --detector socket,family:INET6

Update protocols
----------------
* `dnsimple <http://developer.dnsimple.com/>`_
   Note: requires dnsimple-dyndns to be installed
* `dyndns2 <http://dyn.com/support/developers/api/>`_
* `freedns.afraid.org <http://freedns.afraid.org/>`_

A lot of services on the internet offer some form of compatibility, so check
this list. Some of these are pre-configured for Dyndnsc as a `preset`, see the
section on presets.

Each supported update protocol can be parametrized on the dyndnsc command line
using long options starting with '--updater-' followed by the name of the
protocol:

.. code-block:: bash

    $ dyndnsc --updater-afraid
    $ dyndnsc --updater-dnsimple
    $ dyndnsc --updater-dyndns2

Each of these update protocols supports specific parameters, which might differ
from each other. Each of these additional parameters can specified on the
command line by appending them to the long option described above.

Example to specify `userid` for updater `dyndns2`:

.. code-block:: bash
 
    $ dyndnsc --updater-dyndns2-userid test.nsupdate.info
 

Passing parameters for IP detection
-----------------------------------

Currently, detectors can receive additional command line arguments by
specifying them using comma/colon separated arguments:

.. code-block:: bash

    $ dyndnsc --detector iface,iface:en0,family:INET
    $ dyndnsc --detector webcheck4,url:http://ipv4.nsupdate.info/myip,parser:plain

This is a bit unflexible an might be changed in future versions.

Presets
-------
Dyndnsc comes with a list of pre-configured presets. To see all configured
presets, you can run

.. code-block:: bash

   $ dyndnsc --list-presets

Presets are used to shorten the amount of configuration needed by providing
preconfigured parameters. See the section on the configuration file to see
how to use presets.

Configuration file
------------------

Create a config file test.cfg with this content (no spaces at the left!):

.. code-block:: ini

    [dyndnsc]
    configs = test_ipv4, test_ipv6

    [test_ipv4]
    use_preset = nsupdate.info:ipv4
    updater-hostname = test.nsupdate.info
    updater-userid = test.nsupdate.info
    updater-password = xxxxxxxx

    [test_ipv6]
    use_preset = nsupdate.info:ipv6
    updater-hostname = test.nsupdate.info
    updater-userid = test.nsupdate.info
    updater-password = xxxxxxxx

Now invoke dyndnsc and give this file as configuration:

.. code-block:: bash

    $ dyndnsc --config test.cfg

Custom services
---------------

If you are using a dyndns2 compatible service and need to specify the update
URL explicitly, you can add the argument --updater-dyndns2-url:

.. code-block:: bash

    $ dyndnsc --updater-dyndns2 \
              --updater-dyndns2-hostname=test.dyndns.com \
              --updater-dyndns2-userid=bob \
              --updater-dyndns2-password=fub4r \
              --updater-dyndns2-url=https://dyndns.example.com/nic/update


