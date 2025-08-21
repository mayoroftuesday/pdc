from django.test import TestCase

from ..models import BasePage


class PageTests(TestCase):

    def test_page_title(self):
        """ Confirm that pages use title as string value """
        page = BasePage.objects.create(title="Hello World")
        self.assertEqual(str(page), "Hello World")

    def test_auto_slug(self):
        """ Slug should be auto-generated from title if absent """

        # if a slug is provided, use that
        page = BasePage.objects.create(title="Hello World", slug="hello")
        self.assertEqual(page.slug, "hello")

        # otherwise, generate slug from title
        page_no_slug = BasePage.objects.create(title="Hello World")
        self.assertEqual(page_no_slug.slug, "hello-world")

    def test_auto_summary(self):
        """ Summary should be automatically generated if not provided """

        # If summary is provided, use that
        summary = "Good article"
        page = BasePage.objects.create(summary=summary, content="Hello World")
        self.assertEqual(page.summary, summary)

        # Otherwise take the first paragraph from the article
        html = """
            <p>This is a good article</p>
            <p>Here's something else to read</p>
        """
        page_no_summary = BasePage.objects.create(content=html)
        self.assertEqual(page_no_summary.summary, "This is a good article")
