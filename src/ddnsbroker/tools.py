from ipaddress import IPv6Address, AddressValueError


def normalize_ip(ip: str) -> str:
    try:
        ip6 = IPv6Address(ip)
        ret = ip6.ipv4_mapped or ip6
        return str(ret)
    except AddressValueError:
        return ip
