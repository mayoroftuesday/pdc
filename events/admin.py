from datetime import datetime

from django.contrib import admin
from django.contrib.admin import SimpleListFilter

from .models import EventCategory, Event, EventOccurrence, EventRsvp


class EventStatusFilter(SimpleListFilter):
    """
    Filter for future and past events
    From https://stackoverflow.com/questions/851636/default-filter-in-django-admin  # noqa: E501
    """
    title = 'Event status'
    parameter_name = 'status'

    def lookups(self, request, model_admin):
        return (
            (None, 'Future'),
            ('past', 'Past'),
            ('all', 'All'),
        )

    def choices(self, cl):
        for lookup, title in self.lookup_choices:
            yield {
                'selected': self.value() == lookup,
                'query_string': cl.get_query_string({
                    self.parameter_name: lookup,
                }, []),
                'display': title,
            }

    def queryset(self, request, queryset):
        param = self.value()
        if param == 'Past':
            return queryset.filter(end_date__lte=datetime.today())
        elif param is None:
            return queryset.filter(end_date__gte=datetime.today())
        return queryset


class EventOccurrenceStatusFilter(EventStatusFilter):
    def queryset(self, request, queryset):
        param = self.value()
        if param == 'Past':
            return queryset.filter(date__lte=datetime.today())
        elif param is None:
            return queryset.filter(date__gte=datetime.today())
        return queryset


class EventRsvpInlineAdmin(admin.TabularInline):
    model = EventRsvp


class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'start_date', 'recurrence')
    list_filter = [EventStatusFilter]
    view_on_site = False


class EventOccurrenceAdmin(admin.ModelAdmin):
    list_display = ('title', 'date')
    list_filter = [EventOccurrenceStatusFilter]
    inlines = [EventRsvpInlineAdmin]


admin.site.register(EventCategory)
admin.site.register(Event, EventAdmin)
admin.site.register(EventOccurrence, EventOccurrenceAdmin)
