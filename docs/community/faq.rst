.. _faq:

Frequently Asked Questions
==========================

Python 3 Support?
-----------------

Yes! Here's a list of Python platforms that are officially
supported:

* Python 2.6
* Python 2.7
* Python 3.2
* Python 3.3
* Python 3.4
* PyPy 1.9

Support for Python 2.6 and 3.2 may be dropped at any time.

I get a wrong IPv6 address, why?
--------------------------------
This may be for many different reasons.
You probably are using IPv6 privacy extensions, these extensions
give you a temporary ip that you use to connect to the outside world, but
your router does not allow connections from the outside to this IP.
Then getting your IP via a web interface is impossible.
Currently there is no way for dyndnsc, to find out what of many valid
IPs it should use, if they share the same netmask. As a workaround on unix
like machines, you cann use the `command` detector to gather your IP via a shell
command:

dyndnsc .. --detector=command,command:'ip addr | grep inet6 | grep -v deprecated | grep -v temporary | grep global | perl -pe '"'s/.*?inet6 ([0-9a-f:]+[0-9a-f:]*).*/\1/'"

This command gets all ipv6 addresses, ignores all deprecated, temporary
and non global adresses and hopes that the rest is a single valid v6 address.
