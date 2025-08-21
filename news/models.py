from datetime import date

from django.db import models
from django.urls import reverse

from pages.models import BasePage


class News(BasePage):
    """ News items """
    published = models.DateField(
        blank=True,
        help_text='Leave blank to use today\'s date'
    )

    class Meta:
        verbose_name = 'News Item'
        ordering = ['-published']

    def save(self, *args, **kwargs):
        """ Set fields on save """
        if not self.published:
            self.published = date.today()
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('news:detail', kwargs={
            'slug': self.slug,
            'year': f'{self.published.year}',
            'month': f'{self.published.month:02}',
            'day': f'{self.published.day:02}',
        })
