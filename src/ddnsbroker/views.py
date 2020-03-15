import logging
import re
from ipaddress import IPv4Address, IPv6Address, AddressValueError

from django.utils import timezone
from django.views.generic import View

from ddnsbroker.models import Host
from ddnsbroker.tools.ip import normalize_ip
from ddnsbroker.tools.views import PlainResponse, basic_challenge, basic_authenticate

logger = logging.getLogger(__name__)


class RemoteIpView(View):
    def get(self, request):
        return PlainResponse(normalize_ip(request.META.get('REMOTE_ADDR')))


class NicUpdateView(View):
    def auth_against_host(self, request):
        auth = request.META.get('HTTP_AUTHORIZATION')
        if auth is None:
            logger.debug("received no auth")
            raise Exception()
        username, password = basic_authenticate(auth)

        try:
            host = Host.objects.get(fqdn=username)
            if host.check_password(password):
                return host
        except Host.DoesNotExist:
            pass

        logger.warning("received bad credentials for {}".format(username))
        raise Exception()

    def check_hostname(self, request, username):
        hostname = request.GET.get('hostname')
        if hostname is not None and hostname != username:
            fqdn_patter = re.compile(r"(?=^.{4,253}$)(^((?!-)[a-zA-Z0-9-]{1,63}(?<!-)\.)+[a-zA-Z]{2,63}$)")
            if not fqdn_patter.match(hostname):
                error = 'notfqdn'
            else:
                error = 'nohost'
            logger.warning("rejecting to update {}: {} (user: {})".format(hostname, error, username))
            return error
        return None

    def get_ips_from_request(self, request):
        ipaddrs = request.GET.getlist('myip')
        if not ipaddrs:
            ipaddrs = [normalize_ip(request.META.get('REMOTE_ADDR'))]

        ipv4, ipv6 = None, None
        for ipaddr in ipaddrs:
            try:
                ipv4 = IPv4Address(ipaddr)
            except AddressValueError:
                try:
                    ipv6 = IPv6Address(ipaddr)
                except AddressValueError:
                    pass

        if not ipv4 and not ipv6:
            logger.warning("no valid ipv4/ipv6 found in: {}".format(ipaddrs))
            raise Exception()

        return ipv4, ipv6

    def get(self, request):
        # authenticate
        try:
            host = self.auth_against_host(request)
        except Exception:
            return basic_challenge("Authenticate to update DNS", 'badauth')

        # check if hostname matches username
        error = self.check_hostname(request, host.fqdn)
        if error:
            return PlainResponse(error)

        # get ips from request
        try:
            ipv4, ipv6 = self.get_ips_from_request(request)
        except Exception:
            return PlainResponse("nochg")

        # update host ip and last_update if ip family is enabled
        now = timezone.now()
        if ipv4 and host.ipv4_enabled:
            host.last_ipv4_update = now
            host.ipv4 = str(ipv4)
        if ipv6 and host.ipv6_enabled:
            host.last_ipv6_update = now
            host.ipv6 = str(ipv6)

        ip_changed = host.save(now=now)

        # construct response
        response = "good" if ip_changed else "nochg"

        if ipv4 and ipv6:
            ipstr = "{},{}".format(ipv4, ipv6)
        elif ipv4:
            ipstr = str(ipv4)
        else:
            ipstr = str(ipv6)

        logger.info("{} {} {}".format(host.fqdn, response, ipstr))

        return PlainResponse("{} {}".format(response, ipstr))
