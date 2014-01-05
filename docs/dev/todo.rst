How to Help
===========

Dyndnsc is under active development, and contributions are more than welcome!

#. Check for open issues or open a fresh issue to start a discussion around a bug
   on the `git issue tracker <https://github.com/infothrill/python-dyndnsc/issues>`_.
#. Fork `the repository <https://github.com/infothrill/python-dyndnsc>`_ on GitHub and start making your
   changes to a new branch.
#. Write a test which shows that the bug was fixed.
#. Send a pull request and bug the maintainer until it gets merged and published. :)
   Make sure to add yourself to `AUTHORS <https://github.com/infothrill/python-dyndnsc/blob/master/AUTHORS>`_.

A couple of idioms for contributors
-----------------------------------
These are general guidelines for code contributors.

* keep amount of external dependencies low, i.e. if it can be done using the
  standard library, do it using the standard library
* do not prefer specific operating systems, i.e. even if we love Linux, we
  shall not make other suffer from our personal choice
* write unittests


Loose wishlist of todos
-----------------------
* services: enable updating mutiple different services with the same IP but a different
  hostname. This would provide some form of poor mans redundancy in case one
  of the services is down
* services: http://www.dnsdynamic.org/api.php
   https://username:password@www.dnsdynamic.org/api/?hostname=techno.ns360.info&myip=127.0.0.1
* usability: provide a mechanism to store credentials "safely". For example using
   https://pypi.python.org/pypi/keyring. This should be optional (from an API
   point of view), and it should be easy to setup during a first run
   (interactive use).
* technology: https://pypi.python.org/pypi/pyatomiadns this looks like an RFC2136
  implementation
