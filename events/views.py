from django.contrib.auth.decorators import user_passes_test
from django.core.mail import mail_admins
from django.core.paginator import Paginator
from django.http import Http404
from django.shortcuts import render
from meta.views import Meta

from .models import EventOccurrence
from .forms import RsvpForm


def event_list(request):
    events = EventOccurrence.objects.published(request.user).upcoming()

    paginator = Paginator(events, 5)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    context = {
        'events': page,
        'meta': Meta(
            title='Upcoming Events - Petersburg Democratic Committee',
            description=(
                'Upcoming meetings, special events, and important election '
                'dates',
            )
        ),
    }
    return render(request, 'events/list.html', context)


@user_passes_test(lambda u: u.is_staff)
def event_export(request, id):
    """
    Admin export of event with guest list
    """
    occurrence = EventOccurrence.objects.get(pk=id)
    return render(request, 'events/export.html', {'occurrence': occurrence})


def event_item(request, year, month, day, slug):
    try:
        occurrence = EventOccurrence.objects.published(request.user).get(
            event__slug=slug,
            date__year=year,
            date__month=month,
            date__day=day
        )
    except EventOccurrence.DoesNotExist:
        raise Http404()

    show_thank_you = False

    if request.method == 'POST':
        rsvp_form = RsvpForm(request.POST)
        data = rsvp_form.data
        if rsvp_form.is_valid():
            subject = "RSVP Submitted"
            message = "\n".join([
                f"Event: {occurrence}",
                f"Name: {data['name']}",
                f"Email: {data['email']}",
                f"Phone: {data['phone']}",
                f"Number attending: {data['number_attending']}",
            ])

            mail_admins(subject, message)

            occurrence.eventrsvp_set.create(
                name=data['name'],
                email=data['email'],
                phone=data['phone'],
                number_attending=data['number_attending']
            )

            show_thank_you = True
    else:
        initial_data = {
            'event_occurrence_id': occurrence.id,
        }
        rsvp_form = RsvpForm(initial=initial_data)

    context = {
        'occurrence': occurrence,
        'page': occurrence.event,
        'event': occurrence.event,
        'meta': Meta(
            title=occurrence.event.title,
            description=occurrence.event.summary,
        ),
        'rsvp_form': rsvp_form,
        'show_thank_you': show_thank_you,
    }
    return render(request, 'events/detail.html', context)
