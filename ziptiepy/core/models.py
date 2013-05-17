# python standard modules
from base64 import b64encode, b64decode
import os

# django modules
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.utils.encoding import python_2_unicode_compatible

# other modules
from dirtyfields import DirtyFieldsMixin
from django_fields.fields import EncryptedCharField
import ipaddr
from git import *

# Create your models here.

@python_2_unicode_compatible
class Credential(DirtyFieldsMixin, models.Model):
    """ """
    name = models.CharField(max_length=128)
    description = models.TextField(blank=True)

    username = EncryptedCharField(max_length=128)
    password = EncryptedCharField(max_length=128)

    enable_username = EncryptedCharField(max_length=128, blank=True)
    enable_password = EncryptedCharField(max_length=128, blank=True)

    ip_mappings = models.TextField()

    def __str__(self):
        return "Credential: %s" % self.name

    def match_ip(self, ip):
        match = False
        for x in self.ip_mappings.split(','):
            if x.find('-') > 0:
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

    def get_repo_dir(self):
        return os.path.join(settings.REPO_DIR, str(self.id))

    def make_repo(self):
        repo_dir = self.get_repo_dir()
        if not os.path.exists(repo_dir):
            os.makedirs(repo_dir)
            repo = Repo.init(repo_dir)
            repo.index.commit("Initial Commit")

    def save(self, *args, **kwargs):
        if self.is_dirty() or not self.id:
            super(Device, self).save(*args, **kwargs) # real save()

    def save_config(self, config):
        repo_dir = self.get_repo_dir()
        config_files = []

        self.make_repo() # just make sure a repo exist for working in it.

        for name, data in config.items():
            config_file = os.path.join(repo_dir, name)
            config_files.append(config_file)
            with open(config_file, 'w') as f:
                for line in data:
                    f.write(line.strip() + '\n')

        # add files if new and commit changes to git repo
        repo = Repo(repo_dir)
        repo.index.add(config_files)
        if repo.is_dirty():
            repo.index.commit("Automated Backup")

        return config_files


@receiver(post_save, sender=Device)
def Device_post_save_handler(sender, instance, created, **kwargs):
    if created:
        instance.make_repo()


