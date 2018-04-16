#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

"""
Detect IP v4 or v6 addresses the system uses to talk to outside world.

Original code from
https://github.com/vincentbernat/puppet-workstation/blob/master/modules/system/templates/network/ddns-updater.erb

Refactored/modified by Thomas Waldmann to just detect the IP.
"""

from __future__ import print_function
import errno
import socket

IPV4 = "ipv4"
IPV6_ANY = "ipv6"
IPV6_PUBLIC = "ipv6_public"
IPV6_TMP = "ipv6_tmp"

# reserved IPs for documentation/example purposes
OUTSIDE_IPV4 = "192.0.2.1"
OUTSIDE_IPV6 = "2001:db8::1"

# Not everything is available in Python
if not hasattr(socket, "IPV6_ADDR_PREFERENCES"):
    socket.IPV6_ADDR_PREFERENCES = 72
if not hasattr(socket, "IPV6_PREFER_SRC_TMP"):
    socket.IPV6_PREFER_SRC_TMP = 1
if not hasattr(socket, "IPV6_PREFER_SRC_PUBLIC"):
    socket.IPV6_PREFER_SRC_PUBLIC = 2


class GetIpException(Exception):
    """Generic base class for all exceptions raised here."""


def detect_ip(kind):
    """
    Detect IP address.

    kind can be:
        IPV4 - returns IPv4 address
        IPV6_ANY - returns any IPv6 address (no preference)
        IPV6_PUBLIC - returns public IPv6 address
        IPV6_TMP - returns temporary IPV6 address (privacy extensions)

    This function either returns an IP address (str) or
    raises a GetIpException.
    """
    if kind not in (IPV4, IPV6_PUBLIC, IPV6_TMP, IPV6_ANY):
        raise ValueError("invalid kind specified")

    # We create an UDP socket and connect it to a public host.
    # We query the OS to know what our address is.
    # No packet will really be sent since we are using UDP.
    af = socket.AF_INET if kind == IPV4 else socket.AF_INET6
    s = socket.socket(af, socket.SOCK_DGRAM)
    try:
        if kind in [IPV6_PUBLIC, IPV6_TMP, ]:
            # caller wants some specific kind of IPv6 address (not IPV6_ANY)
            try:
                if kind == IPV6_PUBLIC:
                    preference = socket.IPV6_PREFER_SRC_PUBLIC
                elif kind == IPV6_TMP:
                    preference = socket.IPV6_PREFER_SRC_TMP
                s.setsockopt(socket.IPPROTO_IPV6,
                             socket.IPV6_ADDR_PREFERENCES, preference)
            except socket.error as e:
                if e.errno == errno.ENOPROTOOPT:
                    raise GetIpException("Kernel doesn't support IPv6 address preference")
                else:
                    raise GetIpException("Unable to set IPv6 address preference: %s" % e)

        try:
            outside_ip = OUTSIDE_IPV4 if kind == IPV4 else OUTSIDE_IPV6
            s.connect((outside_ip, 9))
        except (socket.error, socket.gaierror) as e:
            raise GetIpException(str(e))

        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip


if __name__ == "__main__":
    print("IP v4:", detect_ip(IPV4))  # noqa
    print("IP v6 public:", detect_ip(IPV6_PUBLIC))  # noqa
    print("IP v6 tmp:", detect_ip(IPV6_TMP))  # noqa
    print("IP v6 any:", detect_ip(IPV6_ANY))  # noqa
