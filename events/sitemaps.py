from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from .models import EventOccurrence


class EventSitemap(Sitemap):

    def items(self):
        return ['events:index'] + list(EventOccurrence.objects.all())

    def location(self, item):
        if type(item) is str:
            return reverse(item)
        else:
            return super().location(item)
