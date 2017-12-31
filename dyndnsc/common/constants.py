# -*- coding: utf-8 -*-

"""Common constants."""

from .. import __version__

REQUEST_HEADERS_DEFAULT = {
    # dyndns2 standard requires that we set our own user agent:
    "User-Agent": "python-dyndnsc/%s" % __version__,
}
