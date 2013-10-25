[![Build Status](https://travis-ci.org/infothrill/python-dyndnsc.png)](https://travis-ci.org/infothrill/python-dyndnsc)    [![Coverage Status](https://coveralls.io/repos/infothrill/python-dyndnsc/badge.png)](https://coveralls.io/r/infothrill/python-dyndnsc) [![Version](https://pypip.in/v/dyndnsc/badge.png)](https://crate.io/packages/dyndnsc/)   [![Downloads](https://pypip.in/d/dyndnsc/badge.png)](https://crate.io/packages/dyndnsc/)

Description
===========

dyndnsc is both a script to be used directly as well as a re-usable and
hopefully extensible python package for doing updates to dynamic
dns services (http://dyn.com/support/developers/api/).

- updating a dyndns entry is done by a "DynDNS Update Protocol handler"
- detecting IPs, both in DNS or elsewhere is done using IPDetector's
  which all have a detect() method and bookkeeping about changes
- the DynDnsClient uses the Protocol Handler to do the updates and
  the IPDetectors to decide when an update needs to occur

Examples
========

    python dyndnsc.py  --hostname test.dyndns.com --userid bob \
      --method=Iface,netmask:2001:0000::/32,iface:tun0,family:INET6


Installation
============

    # pip install dyndnsc

or, if you want to work using the source tarball:

    # python setup.py install
  

Requirements
============
* Python 2.6, 2.7, 3.2 or 3.3
