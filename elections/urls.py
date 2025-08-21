from django.urls import path

from . import views

app_name = 'elections'
urlpatterns = [
    path('', views.index, name='index'),
    path('vote/', views.vote, name='vote'),
    path('candidates/', views.candidates, name='candidates'),
    path('representatives/', views.representatives, name='representatives'),
    path(
        'representatives/brittany-flowers/',
        views.brittany_flowers,
        name='brittany-flowers'
    ),
    path(
        'representatives/tiffany-buckner/',
        views.tiffany_buckner,
        name='tiffany-buckner'
    ),
    path(
        'representatives/vanessa-crawford/',
        views.vanessa_crawford,
        name='vanessa-crawford'
    ),
    path(
        'representatives/paul-mullin/',
        views.paul_mullin,
        name='paul-mullin'
    ),
]
