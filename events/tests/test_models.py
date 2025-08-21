from datetime import date

from django.test import TestCase

from ..models import Event


class EventTests(TestCase):

    def test_auto_end_date(self):
        """ Use start date as end date unless one is provided """
        y2k = date(2000, 1, 1)
        today = date.today()

        # If end date is provided, use that
        event = Event.objects.create(start_date=y2k, end_date=today)
        self.assertEqual(event.end_date, today)

        # Otherwise use start date
        event = Event.objects.create(start_date=y2k)
        self.assertEqual(event.end_date, y2k)


class EventRecurrenceTests(TestCase):

    def test_no_recurrence(self):
        """ If event doesn't recur, it should only occur on start_date """
        y2k = date(2000, 1, 1)
        today = date.today()

        event = Event.objects.create(
            recurrence=Event.Recurrence.NONE,
            start_date=y2k,
            end_date=today
        )
        self.assertEqual(event.eventoccurrence_set.count(), 1)
        self.assertEqual(event.eventoccurrence_set.first().date, y2k)

    def test_daily_recurrence(self):
        """
        Daily recurrence should create one event
        occurrence every day between start and end
        """
        event = Event.objects.create(
            recurrence=Event.Recurrence.DAILY,
            start_date=date(2000, 1, 1),
            end_date=date(2000, 1, 3)
        )
        occurrences = event.eventoccurrence_set.all()
        self.assertEqual(len(occurrences), 3)
        self.assertEqual(occurrences[0].date, date(2000, 1, 1))
        self.assertEqual(occurrences[1].date, date(2000, 1, 2))
        self.assertEqual(occurrences[2].date, date(2000, 1, 3))

    def test_weekly_recurrence(self):
        """
        Weekly recurrence should create one event
        each week on the same weekday between start and end
        """
        event = Event.objects.create(
            recurrence=Event.Recurrence.WEEKLY,
            start_date=date(2022, 8, 1),
            end_date=date(2022, 9, 1)
        )
        occurrences = event.eventoccurrence_set.all()
        self.assertEqual(len(occurrences), 5)
        self.assertEqual(occurrences[0].date, date(2022, 8, 1))
        self.assertEqual(occurrences[1].date, date(2022, 8, 8))
        self.assertEqual(occurrences[2].date, date(2022, 8, 15))
        self.assertEqual(occurrences[3].date, date(2022, 8, 22))
        self.assertEqual(occurrences[4].date, date(2022, 8, 29))

    def test_monthly_recurrence(self):
        """
        Monthly recurrence should create one event
        each month on the same day between start and end
        """
        event = Event.objects.create(
            recurrence=Event.Recurrence.MONTHLY,
            start_date=date(2022, 1, 27),
            end_date=date(2022, 5, 1)
        )
        occurrences = event.eventoccurrence_set.all()
        self.assertEqual(len(occurrences), 4)
        self.assertEqual(occurrences[0].date, date(2022, 1, 27))
        self.assertEqual(occurrences[1].date, date(2022, 2, 27))
        self.assertEqual(occurrences[2].date, date(2022, 3, 27))
        self.assertEqual(occurrences[3].date, date(2022, 4, 27))

    def test_yearly_recurrence(self):
        """
        Monthly recurrence should create one event
        each year on the same day between start and end
        """
        event = Event.objects.create(
            recurrence=Event.Recurrence.YEARLY,
            start_date=date(2022, 1, 27),
            end_date=date(2025, 1, 1)
        )
        occurrences = event.eventoccurrence_set.all()
        self.assertEqual(len(occurrences), 3)
        self.assertEqual(occurrences[0].date, date(2022, 1, 27))
        self.assertEqual(occurrences[1].date, date(2023, 1, 27))
        self.assertEqual(occurrences[2].date, date(2024, 1, 27))
        assert True

    def test_monthly_nth_week_recurrence(self):
        """
        Monthly nth week recurrence should create one event
        each month on the nth weekday between start and end
        """

        # Monthy event on 4th thursday
        event = Event.objects.create(
            recurrence=Event.Recurrence.MONTHLY_BY_WEEKDAY,
            start_date=date(2022, 1, 27),
            end_date=date(2022, 5, 1)
        )
        occurrences = event.eventoccurrence_set.all()
        self.assertEqual(len(occurrences), 4)
        self.assertEqual(occurrences[0].date, date(2022, 1, 27))
        self.assertEqual(occurrences[1].date, date(2022, 2, 24))
        self.assertEqual(occurrences[2].date, date(2022, 3, 24))
        self.assertEqual(occurrences[3].date, date(2022, 4, 28))

    def test_monthly_last_week_recurrence(self):
        """
        Monthly last week recurrence should create one event
        each month on the last weekday between start and end
        """

        # Monthy event on last thursday
        event = Event.objects.create(
            recurrence=Event.Recurrence.MONTHLY_BY_LAST_WEEKDAY,
            start_date=date(2022, 1, 27),
            end_date=date(2022, 5, 1)
        )
        occurrences = event.eventoccurrence_set.all()
        self.assertEqual(len(occurrences), 4)
        self.assertEqual(occurrences[0].date, date(2022, 1, 27))
        self.assertEqual(occurrences[1].date, date(2022, 2, 24))
        # NOTE: This is the 5th Thursday
        self.assertEqual(occurrences[2].date, date(2022, 3, 31))
        self.assertEqual(occurrences[3].date, date(2022, 4, 28))
