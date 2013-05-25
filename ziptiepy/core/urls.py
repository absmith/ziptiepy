# django modules
from django.conf.urls import patterns, url

# ziptiepy modules
from ziptiepy.core import views

# urls
urlpatterns = patterns('',
    url(r'^$', views.index, name='index')
)