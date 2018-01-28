.. _api:

API Documentation
=================

.. module:: dyndnsc

This part of the documentation should cover all the relevant interfaces of `dyndnsc`.

Main Interface
--------------


.. autoclass:: dyndnsc.DynDnsClient
   :inherited-members:

IP Updaters
-----------
Afraid
~~~~~~
.. automodule:: dyndnsc.updater.afraid

Duckdns
~~~~~~~
.. automodule:: dyndnsc.updater.duckdns

Dyndns2
~~~~~~~
.. automodule:: dyndnsc.updater.dyndns2


IP Detectors
------------

Command
~~~~~~~
.. automodule:: dyndnsc.detector.command

.. autoclass:: dyndnsc.detector.command.IPDetector_Command
  :special-members:  __init__


DNS WAN IP
~~~~~~~~~~
.. automodule:: dyndnsc.detector.dnswanip

.. autoclass:: dyndnsc.detector.dnswanip.IPDetector_DnsWanIp
  :special-members:  __init__

Interface
~~~~~~~~~
.. automodule:: dyndnsc.detector.iface

.. autoclass:: dyndnsc.detector.iface.IPDetector_Iface
   :special-members:  __init__


Socket
~~~~~~
.. automodule:: dyndnsc.detector.socket_ip

.. autoclass:: dyndnsc.detector.socket_ip.IPDetector_Socket
  :special-members:  __init__


Teredo
~~~~~~
.. automodule:: dyndnsc.detector.teredo

.. autoclass:: dyndnsc.detector.teredo.IPDetector_Teredo
  :special-members:  __init__

Web check
~~~~~~~~~
.. automodule:: dyndnsc.detector.webcheck

.. autoclass:: dyndnsc.detector.webcheck.IPDetectorWebCheck
  :special-members:  __init__
