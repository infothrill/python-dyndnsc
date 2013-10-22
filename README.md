[![Build Status](https://travis-ci.org/infothrill/python-dyndnsc.png)](https://travis-ci.org/infothrill/python-dyndnsc)    [![Coverage Status](https://coveralls.io/repos/infothrill/python-dyndnsc/badge.png)](https://coveralls.io/r/infothrill/python-dyndnsc) [![Version](https://pypip.in/v/dyndnsc/badge.png)](https://crate.io/packages/dyndnsc/)   [![Downloads](https://pypip.in/d/dyndnsc/badge.png)](https://crate.io/packages/dyndnsc/)

Description
===========

dyndnsc is both a script to be used directly as well as a re-usable and
hopefully extensible collection of classes for doing updates to dynamic
dns services.

- updating a dyndns entry is done by a "DynDNS Update Protocol handler"
- detecting IPs, both in DNS or elsewhere is done using IPDetector's
  which all have a detect() method and bookkeeping about changes
- the DynDnsClient uses the Protocol Handler to do the updates and
  the IPDetectors to decide when an update needs to occur
- a dummy endless loop ( used for time.sleep() ) repeatedly asks the
  DynDnsClient to make sure everything is fine

Features
=========

- relatively easy to embed in your own application (see main() for an example)
- Growl desktop notification support (optional)

Example use::

    python dyndnsc.py  --hostname test.dyndns.com --userid bob \
      --method=Iface,netmask:2001:0000::/32,iface:tun0,family:INET6


Installation
============
Installation is done using distutils: http://docs.python.org/distutils/

E.g. running
 
  # python setup.py install
  
should be sufficient to install the dyndnsc client module.

Alternatively, you can use pip to install the newest version from the
internet:

  # pip install dyndnsc

Licensing is documented in the file COPYING.
