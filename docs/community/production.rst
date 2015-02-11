.. _production:

Running in production
=====================

Error handling
--------------

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
