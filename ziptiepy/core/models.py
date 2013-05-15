from base64 import b64encode, b64decode
import ipaddr

from django.db import models
from django.conf import settings
from django.utils.encoding import python_2_unicode_compatible

from dirtyfields import DirtyFieldsMixin

# Create your models here.

@python_2_unicode_compatible
class Credential(DirtyFieldsMixin, models.Model):
    """ """
    name = models.CharField(max_length=128)
    descripton = models.TextField(blank=True)

    username = models.CharField(max_length=128)
    password = models.CharField(max_length=128)

    enable_username = models.CharField(max_length=128, blank=True)
    enable_password = models.CharField(max_length=128, blank=True)

    ip_mappings = models.TextField()

    def __str__(self):
        return "Credential: %s" % self.name

    def match_ip(self, ip):
        match = False
        for x in self.ip_mappings.split(','):
            if ip.find('-') > 0:
                ip1 = ipaddr.IPv4Address(x.split('-')[0])
                ip2 = ipaddr.IPv4Address(x.split('-')[1])
                for net in ipaddr.summarize_address_range(ip1,ip2):
                    if ipaddr.IPv4Network(ip) in net:
                        match = True
            else:
                if ipaddr.IPv4Address(ip) == ipaddr.IPv4Address(x):
                    match = True
        return match

    def save(self, *args, **kwargs):
        if self.is_dirty() or not self.id:
            super(Credential, self).save(*args, **kwargs) # real save()



@python_2_unicode_compatible
class Device(DirtyFieldsMixin, models.Model):
    """ """
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True, auto_now_add=True)

    access_ip = models.GenericIPAddressField()
    hostname = models.CharField(max_length=255)

    adapter = models.CharField(max_length=50)

    protocol = models.CharField(max_length=10,
                                    choices=settings.PROTOCOLS)

    access_port = models.IntegerField()

    def __str__(self):
        return "Device: %s" % self.hostname





