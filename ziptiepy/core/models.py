from django.db import models

# Create your models here.
class Device(models.Model):
    """ Base Adapter class all adapters should inherit from this """
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True, auto_now_add=True)
    
    access_ip = models.GenericIPAddressField()
    hostname = models.CharField(max_length=255)
    
    adapter = models.CharField(max_length=50)
    
    
