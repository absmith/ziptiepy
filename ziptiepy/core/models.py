import ipaddr

from django.db import models
from django.conf import settings

# Create your models here.

class Credential(models.Model):
    """ """
    name = models.CharField(max_length=128)
    descripton = models.TextField()
    
    username = models.CharField(max_length=128)
    password = models.TextField()
    
    enable_username = models.CharField(max_length=128)
    enable_password = models.TextField()
    
    ip_mappings = models.TextField()
    
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

class Device(models.Model):
    """ """
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True, auto_now_add=True)
    
    access_ip = models.GenericIPAddressField()
    hostname = models.CharField(max_length=255)
    
    adapter = models.CharField(max_length=50)
    
    protocol = models.CharField(max_length=10,
                                    choices=settings.PROTOCOLS)
    
    access_port = models.IntegerField()

    
    


