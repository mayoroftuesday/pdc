from django.urls import path, re_path

from . import views

app_name = 'news'
urlpatterns = [
    path('', views.news_list, name='index'),
    re_path(
        r'^(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/(?P<day>[0-9]{2})/(?P<slug>[\w-]+)$',  # noqa: E501
        views.news_item,
        name='detail'
    )
]
