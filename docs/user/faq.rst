.. _faq:

Frequently Asked Questions
==========================

Python 3 Support?
-----------------

Yes! In fact, we recommend running on Python3, because a lot of dynamic dns
services provide https interfaces, which are best supported in newer python
versions from a security and performance point of view.

Here's a list of Python platforms that are officially
supported:

* Python 2.7
* Python 3.4
* Python 3.5
* Python 3.6


Is service xyz supported?
-------------------------
To find out wether a certain dynamic dns service is supported by Dyndnsc, you
can either try to identify the protocol involved and see if it is supported by
Dyndnsc by looking the output of 'dyndnsc --help'. Or maybe the service in
question is already listed in the presets ('dyndnsc --list-presets').

I get a wrong IPv6 address, why?
--------------------------------

If you use the "webcheck6" detector and your system has IPv6 privacy extensions,
it'll result in the temporary IPv6 address that you use to connect to the
outside world.

You likely rather want your less private, but static global IPv6 address in
DNS and you can determine it using the "socket" detector.


What about error handling of network issues?
--------------------------------------------

"Hard" errors on the transport level (tcp timeouts, socket erors...) are
not handled and will fail the client. In daemon or loop mode, exceptions are
caught to keep the client alive (and retries will be issued at a later time).
