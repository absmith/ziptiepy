# django modules
from django.shortcuts import render

# ziptiepy modules
from ziptiepy.core.models import Device

# Create your views here.

def index(request, template='core/index.html'):
    devices = Device.objects.all()
    context = { 
                'devices': devices,
               }
    return render(request, template, context)