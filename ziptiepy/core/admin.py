# django modules
from django.contrib import admin

# ziptiepy modules
from ziptiepy.core.forms import CredentialForm
from ziptiepy.core.models import Credential, Device

class CredentialAdmin(admin.ModelAdmin):
    form = CredentialForm


admin.site.register(Credential, CredentialAdmin)
admin.site.register(Device)
