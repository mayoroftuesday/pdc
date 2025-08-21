from django.urls import path, re_path

from . import views

app_name = 'events'
urlpatterns = [
    path('', views.event_list, name='index'),
    re_path(
        r'^(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/(?P<day>[0-9]{2})/(?P<slug>[\w-]+)$',  # noqa: E501
        views.event_item,
        name='detail'
    ),
    re_path(r'^export/(?P<id>\d+)$', views.event_export, name='export'),
]
