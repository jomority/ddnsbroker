from ipaddress import IPv4Address, IPv4Network, IPv6Address, IPv6Network

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.core.validators import RegexValidator, MaxValueValidator, URLValidator
from django.db import models
from django.utils import timezone


class Host(models.Model):
    fqdn = models.CharField(
        verbose_name="FQDN",
        max_length=255,
        validators=[
            RegexValidator(
                regex=r"(?=^.{4,253}$)(^((?!-)[a-zA-Z0-9-]{1,63}(?<!-)\.)+[a-zA-Z]{2,63}$)",
                # https://stackoverflow.com/a/20204811
                message='Invalid FQDN: only "a-z", "0-9" and "-" is allowed'
            ),
        ],
        unique=True,
        help_text="Is also used as HTTP Basic Auth username.")

    secret = models.CharField(max_length=128, help_text="Will be hashed if changed.")
    __original_secret = None

    ipv4_enabled = models.BooleanField(verbose_name="IPv4 enabled", default=True)
    ipv6_enabled = models.BooleanField(verbose_name="IPv6 enabled", default=True)

    ipv4 = models.GenericIPAddressField(verbose_name="IPv4", protocol='IPv4', null=True, blank=True)
    ipv6 = models.GenericIPAddressField(verbose_name="IPv6", protocol='IPv6', null=True, blank=True)
    __original_ipv4 = None
    __original_ipv6 = None

    last_ipv4_update = models.DateTimeField(null=True, blank=True, editable=False)
    last_ipv6_update = models.DateTimeField(null=True, blank=True, editable=False)
    last_ipv4_change = models.DateTimeField(null=True, blank=True, editable=False)
    last_ipv6_change = models.DateTimeField(null=True, blank=True, editable=False)

    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.fqdn

    class Meta(object):
        ordering = ('fqdn',)

    def __init__(self, *args, **kwargs):
        super(Host, self).__init__(*args, **kwargs)
        self.__original_secret = self.secret
        self.__original_ipv4 = self.ipv4
        self.__original_ipv6 = self.ipv6

    def save(self, *args, **kwargs):
        if self.secret != self.__original_secret:
            self.generate_secret(secret=self.secret, save=False)

        ip_changed = False
        now = timezone.now()
        if self.ipv4 != self.__original_ipv4 and self.ipv4 != "":
            self.last_ipv4_change = now
            ip_changed = True
        if self.ipv6 != self.__original_ipv6 and self.ipv6 != "":
            self.last_ipv6_change = now
            ip_changed = True

        super(Host, self).save(*args, **kwargs)

        self.__original_secret = self.secret
        self.__original_ipv4 = self.ipv4
        self.__original_ipv6 = self.ipv6

        if ip_changed:
            for record in Record.objects.filter(host=self):
                record.save()

    def generate_secret(self, secret=None, save=True):
        if secret is None:
            secret = get_user_model().objects.make_random_password()
        self.secret = make_password(secret)
        if save:
            self.save()
        return secret


class UpdateService(models.Model):
    name = models.CharField(max_length=32, unique=True)

    url = models.CharField(
        verbose_name="URL",
        max_length=2048,
        validators=[URLValidator(schemes=['http', 'https'])],
        help_text="E.g. \"https://dyndns.example.com/nic/update\"")

    username_is_fqdn = models.BooleanField(
        verbose_name="Username is FQDN",
        default=False,
        help_text="Whether the HTTP Basic Auth username is the record FQDN.")

    def __str__(self):
        return self.name

    class Meta(object):
        ordering = ('name',)


class Record(models.Model):
    host = models.ForeignKey(Host, on_delete=models.PROTECT)

    fqdn = models.CharField(
        verbose_name="FQDN",
        max_length=255,
        validators=[
            RegexValidator(
                regex=r"(?=^.{4,253}$)(^((?!-)[a-zA-Z0-9-]{1,63}(?<!-)\.)+[a-zA-Z]{2,63}$)",
                # https://stackoverflow.com/a/20204811
                message='Invalid FQDN: only "a-z", "0-9" and "-" is allowed'
            ),
        ],
        blank=True)

    ipv4_enabled = models.BooleanField(verbose_name="IPv4 enabled", default=True)
    ipv6_enabled = models.BooleanField(verbose_name="IPv6 enabled", default=True)

    ipv4_netmask = models.PositiveSmallIntegerField(
        verbose_name="IPv4 netmask",
        default=32,
        validators=[MaxValueValidator(32)],
        help_text="IPv4 record uses network prefix of the host. Set to 32 to use whole IP.")
    ipv4_host_id = models.GenericIPAddressField(
        verbose_name="IPv4 host identifier",
        protocol='IPv4', default="0.0.0.0",
        help_text="IPv4 record uses this host identifier, e.g. \"0.0.0.42\".")
    ipv6_netmask = models.PositiveSmallIntegerField(
        verbose_name="IPv6 netmask",
        default=128,
        validators=[MaxValueValidator(128)],
        help_text="IPv6 record uses network prefix of the host. Set to 128 to use whole IP.")
    ipv6_host_id = models.GenericIPAddressField(
        verbose_name="IPv6 host identifier",
        protocol='IPv6', default="::",
        help_text="IPv6 record uses this host identifier, e.g. \"::4042:42FF:FE42:4242\".")

    effective_ipv4 = models.GenericIPAddressField(
        verbose_name="effective IPv4",
        protocol='IPv4',
        null=True, blank=True, editable=False
    )
    effective_ipv6 = models.GenericIPAddressField(
        verbose_name="effective IPv6",
        protocol='IPv6',
        null=True, blank=True, editable=False
    )
    __original_effective_ipv4 = None
    __original_effective_ipv6 = None

    service = models.ForeignKey(UpdateService, on_delete=models.PROTECT)

    username = models.CharField(max_length=255, blank=True)
    password = models.CharField(max_length=255)

    last_ipv4_update = models.DateTimeField(null=True, blank=True, editable=False)
    last_ipv6_update = models.DateTimeField(null=True, blank=True, editable=False)
    last_ipv4_change = models.DateTimeField(null=True, blank=True, editable=False)
    last_ipv6_change = models.DateTimeField(null=True, blank=True, editable=False)

    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.fqdn

    class Meta(object):
        unique_together = (('host', 'fqdn'),)
        ordering = ('host', 'fqdn')

    def __init__(self, *args, **kwargs):
        super(Record, self).__init__(*args, **kwargs)
        self.__original_effective_ipv4 = self.effective_ipv4
        self.__original_effective_ipv6 = self.effective_ipv6

    def save(self, *args, **kwargs):
        if not self.fqdn:
            self.fqdn = self.host.fqdn
        if self.service.username_is_fqdn:
            self.username = self.fqdn

        self.__update_effective_ipv4()
        self.__update_effective_ipv6()

        now = timezone.now()
        if self.effective_ipv4 != self.__original_effective_ipv4:
            self.last_ipv4_change = now
            # TODO: send update, if successful update last_ipv4_update
        if self.effective_ipv6 != self.__original_effective_ipv6:
            self.last_ipv6_change = now
            # TODO: send update, if successful update last_ipv6_update

        super(Record, self).save(*args, **kwargs)

        self.__original_effective_ipv4 = self.effective_ipv4
        self.__original_effective_ipv6 = self.effective_ipv6

    def __update_effective_ipv4(self) -> None:
        if self.host.ipv4 is None or self.host.ipv4 is "":
            self.effective_ipv4 = None
            return

        host_id: int = int(IPv4Address(self.ipv4_host_id))
        host_id_short: int = host_id & ((1 << 32 - self.ipv4_netmask) - 1)

        network: str = "{}/{}".format(self.host.ipv4, self.ipv4_netmask)
        network_address: IPv4Address = IPv4Network(network, strict=False).network_address

        self.effective_ipv4 = str(network_address + host_id_short)

    def __update_effective_ipv6(self) -> None:
        if self.host.ipv6 is None or self.host.ipv6 is "":
            self.effective_ipv6 = None
            return

        host_id: int = int(IPv6Address(self.ipv6_host_id))
        host_id_short: int = host_id & ((1 << 128 - self.ipv6_netmask) - 1)

        network: str = "{}/{}".format(self.host.ipv6, self.ipv6_netmask)
        network_address: IPv6Address = IPv6Network(network, strict=False).network_address

        self.effective_ipv6 = str(network_address + host_id_short)
