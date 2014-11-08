# -*- coding: utf-8 -*-
"""
common constants
"""

import dyndnsc

REQUEST_HEADERS_DEFAULT = {
    # dyndns2 standard requires that we set our own user agent:
    'User-Agent': 'python-dyndnsc/%s' % dyndnsc.__version__,
}
