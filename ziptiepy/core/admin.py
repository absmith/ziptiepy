from django import forms
from django.contrib import admin

from ziptiepy.core.models import Credential, Device


class CredentialAdminForm(forms.ModelForm):
    class Meta:
        model = Credential
        widgets = {
                    'password': forms.PasswordInput,
                    'enable_password': forms.PasswordInput,
        }

class CredentialAdmin(admin.ModelAdmin):
    form = CredentialAdminForm

admin.site.register(Credential, CredentialAdmin)
admin.site.register(Device)