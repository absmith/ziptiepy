from django.db import models

# Create your models here.


class Generic(Models.Model):
    """ Base Adapter class all adapters should inherit from this """
    access_ip = models.GenericIPAdressField()
    
    class Meta:
        abstract = True
        