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


What about error handling of network issues?
--------------------------------------------

Connection errors and timeout errors on the socket level and http level are
mostly handled as transient and simply ignored, i.e. updating and/or detecting
an IP will fail with a log message but the client should remain active and
retry later.

Some errors are not handled gracefully, for example if there is an SSL handshake
issue when using a https connection, dyndnsc will typically fail.

Thus, depending on your needs, it might be required to put the dyndnsc client
inside a retry loop to run it in a completely unattended way. Don't
be fooled by the --daemon option, it is available, but the design of the
dyndnsc program does not provide longevity guarantees. Feel free to contribute
some by sending pull requests!
