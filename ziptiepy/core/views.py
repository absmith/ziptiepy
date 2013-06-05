# django modules
from django.shortcuts import render
from django.template import RequestContext
from django.views.generic.detail import DetailView

# ziptiepy modules
from ziptiepy.core.models import Device

# Create your views here.

def index(request, template='core/index.html'):
  devices = Device.objects.all()
  context = RequestContext(request, {
        'devices': devices,
         })
  return render(request, template, context)

class DeviceDetailView(DetailView):
  model = Device


