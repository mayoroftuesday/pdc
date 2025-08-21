from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class PDCSitemap(Sitemap):

    def items(self):
        return [
            'home',
            'act',
            'info',
            'about',
            'volunteer',
            'join',
            'donate',
            'contact',
        ]

    def location(self, item):
        return reverse(item)
