from datetime import date

from django.test import TestCase

from ..models import News


class NewsTests(TestCase):

    def test_auto_publish_date(self):
        """ Publish date should be automatically set if not provided """

        # If date is provided, use that
        y2k = date(2000, 1, 1)
        news = News.objects.create(published=y2k)
        self.assertEqual(news.published, y2k)

        # Otherwise use today's date
        news_no_date = News.objects.create()
        self.assertEqual(news_no_date.published, date.today())
