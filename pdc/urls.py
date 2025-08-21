from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import path, include

from . import views
from .sitemaps import PDCSitemap
from events.sitemaps import EventSitemap
from news.sitemaps import NewsSitemap
from pages.sitemaps import PageSitemap
from elections.sitemaps import ElectionsSitemap

sitemaps = {
    'static': PDCSitemap,
    'events': EventSitemap,
    'news': NewsSitemap,
    'pages': PageSitemap,
    'elections': ElectionsSitemap
}

urlpatterns = [
    # home
    path('', views.home, name='home'),

    # static pages
    path('act/', views.act, name='act'),
    path('info/', views.info, name='info'),
    path('about/', views.about, name='about'),
    path('join/', views.join, name='join'),
    path('donate/', views.donate, name='donate'),
    path('contact/', views.contact, name='contact'),
    path('volunteer/', views.volunteer, name='volunteer'),

    # apps
    path('news/', include('news.urls')),
    path('events/', include('events.urls')),
    path('pages/', include('pages.urls')),
    path('elections/', include('elections.urls')),

    # admin
    path('admin/', admin.site.urls),

    # sitemap
    path(
        'sitemap.xml',
        sitemap,
        {'sitemaps': sitemaps},
        name='django.contrib.sitemaps.views.sitemap'
    )
]

if settings.DEBUG:
    urlpatterns.extend(
        static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    )
