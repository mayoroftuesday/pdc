from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from .models import News


class NewsSitemap(Sitemap):

    def items(self):
        return ['news:index'] + list(News.objects.all())

    def lastmod(self, item):
        if type(item) is str:
            return None
        else:
            return item.published

    def location(self, item):
        if type(item) is str:
            return reverse(item)
        else:
            return super().location(item)
