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

Dyndnsc exposes all options through the command line interface, however,
we do recommend using a configuration file.
Here is an example to update an IPv4 record on nsupdate.info with web
based IP autodetection:

.. code-block:: bash

    $ dyndnsc --updater-dyndns2 \
              --updater-dyndns2-hostname  test.nsupdate.info \
              --updater-dyndns2-userid    test.nsupdate.info \
              --updater-dyndns2-password  XXXXXXXX \
              --updater-dyndns2-url       https://nsupdate.info/nic/update \
              --detector-webcheck4 \
              --detector-webcheck4-url    https://ipv4.nsupdate.info/myip \
              --detector-webcheck4-parser plain


Updating an IPv6 address when using `Miredo <http://www.remlab.net/miredo/>`_:

.. code-block:: bash

    $ dyndnsc --updater-dyndns2 \
              --updater-dyndns2-hostname test.nsupdate.info \
              --updater-dyndns2-userid   test.nsupdate.info \
              --updater-dyndns2-password XXXXXXXX \
              --detector-teredo

Updating an IPv6 record on nsupdate.info with interface based IP detection:

.. code-block:: bash

    $ dyndnsc --updater-dyndns2 \
              --updater-dyndns2-hostname test.nsupdate.info \
              --updater-dyndns2-userid   test.nsupdate.info \
              --updater-dyndns2-password XXXXXXXX \
              --detector-socket \
              --detector-socket-family   INET6

Update protocols
----------------
Dyndnsc supports several different methods for updating dynamic DNS services:

* `dnsimple <https://developer.dnsimple.com/>`_
   Note: requires python package `dnsimple-dyndns <https://pypi.python.org/pypi/dnsimple-dyndns>`_ to be installed
* `duckdns <https://www.duckdns.org/>`_
* `dyndns2 <https://help.dyn.com/remote-access-api/>`_
* `freedns.afraid.org <https://freedns.afraid.org/>`_

A lot of services on the internet offer some form of compatibility, so check
against this list. Some of these external services are pre-configured for
Dyndnsc as a `preset`, see the section on presets.

Each supported update protocol can be parametrized on the dyndnsc command line
using long options starting with '--updater-' followed by the name of the
protocol:

.. code-block:: bash

    $ dyndnsc --updater-afraid
    $ dyndnsc --updater-dnsimple
    $ dyndnsc --updater-duckdns
    $ dyndnsc --updater-dyndns2

Each of these update protocols supports specific parameters, which might differ
from each other. Each of these additional parameters can specified on the
command line by appending them to the long option described above.

Example to specify `token` for updater `duckdns`:

.. code-block:: bash

    $ dyndnsc --updater-duckdns-token 847c0ffb-39bd-326f-b971-bfb3d4e36d7b


Detecting the IP
----------------
*Dyndnsc* ships a couple of "detectors" which are capable of finding an IP
address through different means.

Detectors may need additional parameters to work properly. Additional parameters
can be specified on the command line similarly to the update protocols.

.. code-block:: bash

    $ dyndnsc --detector-iface \
              --detector-iface-iface  en0 \
              --detector-iface-family INET

    $ dyndnsc --detector-webcheck4 \
              --detector-webcheck4-url    http://ipv4.nsupdate.info/myip \
              --detector-webcheck4-parser plain

Some detectors require additional python dependencies:

* *iface*, *teredo* detectors require `netifaces <https://pypi.python.org/pypi/netifaces>`_ to be installed

Presets
-------
*Dyndnsc* comes with a list of pre-configured presets. To see all configured
presets, you can run

.. code-block:: bash

   $ dyndnsc --list-presets

Presets are used to shorten the amount of configuration needed by providing
preconfigured parameters. For convenience, Dyndnsc ships some built-in presets
but this list can be extended by yourself by adding them to the configuration
file. Each preset has a section in the ini file called '[preset:NAME]'.
See the section on the configuration file to see how to use presets.

Note: Presets can currently only be used in a configuration file. There is
currently no support to select a preset from the command line.

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


Plugins
-------
*Dyndnsc* supports plugins which can be notified when a dynamic DNS entry was
changed. Currently, only two plugins exist:

* `dyndnsc-growl <https://pypi.python.org/pypi/dyndnsc-growl>`_
* `dyndnsc-macosnotify <https://pypi.python.org/pypi/dyndnsc-macosnotify>`_

The list of plugins that are installed and available in your environment will
be listed in the command line help. Each plugin command line option starts with
'--with-'.
