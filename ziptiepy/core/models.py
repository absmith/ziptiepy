from django.db import models
from django.conf import settings

# Create your models here.

class Credentials(models.Model):
    """ """
    name = models.CharField(max_length=128)
    descripton = models.TextField()
    
    username = models.CharField(max_length=128)
    password = models.TextField()
    

class Device(models.Model):
    """ """
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True, auto_now_add=True)
    
    access_ip = models.GenericIPAddressField()
    hostname = models.CharField(max_length=255)
    
    adapter = models.CharField(max_length=50)
    
    protocol = models.CharField(max_length=10,
                                    choices=settings.PROTOCOLS)
    
    access_port = models.IntergerField()
