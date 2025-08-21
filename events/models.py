from datetime import datetime
from dateutil.relativedelta import relativedelta, MO, TU, WE, TH, FR, SA, SU
from math import ceil
import calendar

from django.db import models
from django.urls import reverse

from pages.models import BasePage


class EventCategory(models.Model):

    class Color(models.TextChoices):
        GRAY = ('category-gray', 'Gray')
        BLUE = ('category-blue', 'Blue')
        GREEN = ('category-green', 'Green')
        YELLOW = ('category-yellow', 'Yellow')
        ORANGE = ('category-orange', 'Orange')
        RED = ('category-red', 'Red')
        PURPLE = ('category-purple', 'Purple')
    label = models.CharField(max_length=15)
    color = models.CharField(
        max_length=20,
        choices=Color.choices,
        default=Color.GRAY
    )

    class Meta:
        verbose_name_plural = 'Event Categories'

    def __str__(self):
        return self.label


class Event(BasePage):
    """ An event, or series of events"""

    class Meta:
        ordering = ['start_date', 'time']

    class Recurrence(models.TextChoices):
        NONE = ('N', 'None')
        DAILY = ('D', 'Daily')
        WEEKLY = ('W', 'Weekly')
        YEARLY = ('Y', 'Yearly')
        MONTHLY = ('M', 'Monthly')
        MONTHLY_BY_WEEKDAY = ('MW', 'Monthly on nth weekday')
        MONTHLY_BY_LAST_WEEKDAY = ('MLW', 'Monthly on last weekday')

    start_date = models.DateField()
    is_all_day = models.BooleanField(default=True)
    time = models.TimeField(blank=True, null=True)
    recurrence = models.CharField(
        max_length=3,
        choices=Recurrence.choices,
        default=Recurrence.NONE,
    )
    end_date = models.DateField(
        blank=True,
        null=True,
        help_text=(
            "Last day for recurring events. "
            "Leave blank for one-time events to use the same as start date"
        )
    )
    location = models.CharField(max_length=255, blank=True, null=True)
    category = models.ForeignKey(
        EventCategory,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    include_rsvp = models.BooleanField(default=False)

    def _get_weekday(self):
        weekday = self.start_date.weekday()
        weekdays = {
            calendar.MONDAY: MO,
            calendar.TUESDAY: TU,
            calendar.WEDNESDAY: WE,
            calendar.THURSDAY: TH,
            calendar.FRIDAY: FR,
            calendar.SATURDAY: SA,
            calendar.SUNDAY: SU,
        }
        return weekdays[weekday]

    def create_occurrences(self):

        # clear old event occurrences
        for occurrence in self.eventoccurrence_set.all():
            occurrence.delete()

        # choose a different delta based on recurrence
        delta = None
        if self.recurrence == Event.Recurrence.DAILY:
            delta = relativedelta(days=1)
        elif self.recurrence == Event.Recurrence.WEEKLY:
            delta = relativedelta(weeks=1)
        elif self.recurrence == Event.Recurrence.MONTHLY:
            delta = relativedelta(months=1)
        elif self.recurrence == Event.Recurrence.YEARLY:
            delta = relativedelta(years=1)
        elif self.recurrence == Event.Recurrence.MONTHLY_BY_WEEKDAY:
            weekday = self._get_weekday()
            week_number = ceil(self.start_date.day / 7)
            delta = relativedelta(
                months=1,
                day=1,
                weekday=weekday(week_number)
            )
        elif self.recurrence == Event.Recurrence.MONTHLY_BY_LAST_WEEKDAY:
            weekday = self._get_weekday()
            delta = relativedelta(
                months=2,
                day=1,
                days=-1,
                weekday=weekday(-1)
            )

        # create event occurrences
        event_date = self.start_date
        while event_date <= self.end_date:
            self.eventoccurrence_set.create(date=event_date)
            if not delta:
                break
            event_date += delta

    def save(self, *args, **kwargs):
        if not self.end_date:
            self.end_date = self.start_date
        super().save(*args, **kwargs)

        self.create_occurrences()


class UpcomingEventsQuerySet(models.QuerySet):
    def upcoming(self):
        return self.filter(date__gte=datetime.today())

    def published(self, user=None):
        if user is None or user.is_staff is False:
            return self.filter(event__status=BasePage.Status.PUBLISHED)
        else:
            return self


class EventOccurrence(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    date = models.DateField()

    class Meta:
        ordering = ['date', 'event__time']

    # managers
    objects = UpcomingEventsQuerySet.as_manager()

    @property
    def title(self):
        return self.event.title

    @property
    def total_attending(self):
        aggregate = self.eventrsvp_set.aggregate(
            models.Sum('number_attending')
        )
        return aggregate['number_attending__sum']

    @property
    def is_past(self):
        return self.date < datetime.today().date()

    def get_absolute_url(self):
        return reverse('events:detail', kwargs={
            'slug': self.event.slug,
            'year': f'{self.date.year}',
            'month': f'{self.date.month:02}',
            'day': f'{self.date.day:02}',
        })

    def __str__(self):
        return self.title


class EventRsvp(models.Model):
    """
    Records an RSVP for an event occurrence
    """
    event_occurrence = models.ForeignKey(
        EventOccurrence, on_delete=models.CASCADE
    )

    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    number_attending = models.IntegerField(default=1)

    def __str__(self):
        plus = self.number_attending - 1
        label = f"{self.name} <{self.email}>"
        if plus:
            label += f" (+{plus})"
        return label
