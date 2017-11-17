from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^registry/$', views.register, name='register'),
    url(r'^registry/multiple$', views.register_multiple, name='register_multiple'),
    url(r'^registry/(?P<object_id>[0-9]+)/$', views.detail, name='details')
]