from django.contrib import admin

from ziptiepy.core.models import Credential, Device

admin.site.register(Credential)
admin.site.register(Device)