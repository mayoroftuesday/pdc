from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.utils.html import strip_tags

from ckeditor.fields import RichTextField


class PublishedManager(models.Manager):
    """
    Exposes a published() function on the object manager
    which takes an optional user.

    If the user is an admin, it will return all items. Otherwise
    it will return only published.
    """

    def published(self, user=None):
        if user is None or user.is_staff is False:
            return self.filter(status=BasePage.Status.PUBLISHED)
        else:
            return self


class BasePage(models.Model):
    """
    Base model for pages with title, slug, rich text content, and a summary
    """

    class Status(models.IntegerChoices):
        DRAFT = (0, 'Draft')
        PUBLISHED = (1, 'Published')

    status = models.IntegerField(
        choices=Status.choices,
        default=Status.DRAFT
    )
    title = models.CharField(max_length=50)
    content = RichTextField(blank=True, null=True)
    summary = models.CharField(
        max_length=1024,
        blank=True,
        help_text='Leave blank to auto generate'
    )
    slug = models.SlugField(
        blank=True,
        help_text='Leave blank to auto generate'
    )

    # managers
    objects = PublishedManager()

    @property
    def is_draft(self):
        return self.status == BasePage.Status.DRAFT

    @property
    def is_published(self):
        return self.status == BasePage.Status.PUBLISHED

    def save(self, *args, **kwargs):
        """ Set slug on save """
        if not self.slug:
            self.slug = slugify(self.title)
        if not self.summary:
            all_lines = strip_tags(self.content).split('\n')
            content_lines = [
                line.strip()
                for line in all_lines
                if line.strip()
            ]
            if content_lines:
                self.summary = content_lines[0]
            else:
                self.summary = ''
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        raise NotImplementedError()

    def __str__(self):
        return self.title


class Page(BasePage):
    """ Generic rich text page """
    def get_absolute_url(self):
        return reverse('pages:page', kwargs={'slug': self.slug})
