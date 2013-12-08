import sys


if sys.version_info < (3, 3):
    import IPy

    def address(addr):
        return IPy.IP(addr)

    def network(addr):
        return IPy.IP(addr)

else:
    import ipaddress

    def address(addr):
        return ipaddress.ip_address(addr)

    def network(addr):
        return ipaddress.ip_network(addr)
