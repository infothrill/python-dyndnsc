Loose wishlist of things to achieve.

Please consult https://github.com/infothrill/python-dyndnsc/issues for actual
issues/problems with the existing code.

Dyndns update services support
------------------------------
* enable updating mutiple different services with the same IP but a different
  hostname. This would provide some form of poor mans redundancy in case one
  of the services is down
* http://www.dnsdynamic.org/api.php
   https://username:password@www.dnsdynamic.org/api/?hostname=techno.ns360.info&myip=127.0.0.1
* dnsimple.com, see also existing project at
   https://github.com/rafaelmartins/dnsimple-dyndns

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
