from django.db import models
from solo.models import SingletonModel


class Announcement(SingletonModel):
    active = models.BooleanField(default=False)
    title = models.CharField(max_length=50)
    content = models.CharField(max_length=255)
    cta_text = models.CharField(max_length=15)
    cta_link = models.URLField()

    def __str__(self):
        return "Announcement"

    class Meta:
        verbose_name = "Announcement"
