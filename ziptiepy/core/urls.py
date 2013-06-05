# django modules
from django.conf.urls import patterns, url

# ziptiepy modules
from ziptiepy.core import views
from ziptiepy.core.views import index, DeviceDetailView
# urls
urlpatterns = patterns('',
    url(r'^$', index, name='index'),
    url(r'device/(?P<pk>\d+)', DeviceDetailView.as_view(), 
                              name='device-detail'),
)