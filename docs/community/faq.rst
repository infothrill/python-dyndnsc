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

If you use the "webcheck6" detector and your system has IPv6 privacy extensions,
it'll result in the temporary IPv6 address that you use to connect to the
outside world.

You likely rather want your less private, but static global IPv6 address in
DNS and you can determine it using the "socket" detector.
