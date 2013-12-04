Loose wishlist of things to achieve.

Please consult https://github.com/infothrill/python-dyndnsc/issues for actual
issues/problems with the existing code.

Python version related
----------------------

* python 3.3 introduced a new stdlib module 'ipaddress'
   http://docs.python.org/3/library/ipaddress.html
  potentially replacing the need for IPy. It's also backported for older python
  versions at https://pypi.python.org/pypi/ipaddress


Dyndns update services support
------------------------------
* enable updating mutiple different services with the same IP but a different
  hostname. This would provide some form of poor mans redundancy in case one
  of the services is down
* http://www.dnsdynamic.org/api.php
   https://username:password@www.dnsdynamic.org/api/?hostname=techno.ns360.info&myip=127.0.0.1

Usability
---------
* provide a mechanism to store credentials "safely". For example using
   https://pypi.python.org/pypi/keyring. This should be optional (from an API
   point of view), and it should be easy to setup during a first run
   (interactive use).

Technology to investigate
-------------------------
* https://pypi.python.org/pypi/pyatomiadns this looks like an RFC2136
  implementation
