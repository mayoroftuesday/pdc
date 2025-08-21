from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class ElectionsSitemap(Sitemap):

    def items(self):
        return [
            'elections:index',
            'elections:vote',
            'elections:candidates',
            'elections:representatives',
            'elections:brittany-flowers',
            'elections:tiffany-buckner',
            'elections:vanessa-crawford',
            'elections:paul-mullin',
        ]

    def location(self, item):
        return reverse(item)
