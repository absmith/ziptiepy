# django modules
from django import forms

# ziptiepy modules
from ziptiepy.core.models import Credential

class CredentialForm(forms.ModelForm):
    """
    
    """
    class Meta:
        model = Credential
        fields = ('name', 'description', 'username',
                  'password', 'password2', 'enable_username',
                  'enable_password', 'enable2', 'ip_mappings')
        widgets = {
            'password': forms.PasswordInput(render_value=True),
            'enable_password': forms.PasswordInput(render_value=True),
        }
    
    error_messages = {
        'password_mismatch': "The two password fields didn't match.",
    }

    password2 = forms.CharField(label="Password (again)", 
                                widget=forms.PasswordInput)

    enable2 = forms.CharField(label="Enable Password (again)",
                                widget=forms.PasswordInput, required=False)
    
    def clean_password2(self):
        password1 = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(
                    self.error_messages['password_mismatch'])
        return password2
    
    def clean_enable2(self):
        enable1 = self.cleaned_data.get('enable_password')
        enable2 = self.cleaned_data.get('enable2')
        if enable1 and enable2:
            if enable1 != enable2:
                raise forms.ValidationError(
                    self.error_messages['password_mismatch'])
        return enable2

    