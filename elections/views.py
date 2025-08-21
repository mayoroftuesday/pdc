from django.shortcuts import render
from meta.views import Meta

from events.models import EventOccurrence


def index(request):
    context = {
        'meta': Meta(
            title='Upcoming Elections - Petersburg Democratic Committee',
            description='Upcoming elections and key races'
        ),
    }
    return render(request, 'elections/index.html', context)


def representatives(request):
    context = {
        'meta': Meta(
            title=(
                'Your Democratic Representatives - '
                'Petersburg Democratic Committee'
            ),
            description=(
                'Current Democratic elected officials for federal and state '
                'positions'
            )
        ),
    }
    return render(request, 'elections/representatives.html', context)


def candidates(request):
    context = {
        'meta': Meta(
            title=(
                'Meet the Candidates - '
                'Petersburg Democratic Committee'
            ),
            description=(
                'Learn more about the Democratic candidates running for '
                'office in upcoming elections'
            )
        ),
    }
    return render(request, 'elections/candidates.html', context)


def vote(request):

    events = EventOccurrence.objects.published(request.user)
    upcoming_events = (
        events
        .upcoming()
        .filter(event__category__label__in=['Elections', 'Primaries'])
        [:5]
    )

    context = {
        'meta': Meta(
            title='Vote - Petersburg Democratic Committee',
            description=(
                'Make sure you are registered and know how and where to vote'
            ),
        ),
        'events': upcoming_events,
    }
    return render(request, 'elections/vote.html', context)


def brittany_flowers(request):
    context = {
        'meta': Meta(
            title='Brittany Flowers - Petersburg Democratic Committee',
            description='Petersburg Commissioner of Revenue Brittany Flowers',
        ),
    }
    return render(request, 'elections/bios/brittany_flowers.html', context)


def tiffany_buckner(request):
    context = {
        'meta': Meta(
            title='Tiffany Buckner - Petersburg Democratic Committee',
            description='Petersburg Commonwealth\'s Attorney Tiffany Buckner',
        ),
    }
    return render(request, 'elections/bios/tiffany_buckner.html', context)


def vanessa_crawford(request):
    context = {
        'meta': Meta(
            title='Vanessa Crawford - Petersburg Democratic Committee',
            description='Petersburg Sheriff Vanessa Crawford',
        ),
    }
    return render(request, 'elections/bios/vanessa_crawford.html', context)


def paul_mullin(request):
    context = {
        'meta': Meta(
            title='Paul Mullin - Petersburg Democratic Committee',
            description='Petersburg Treasurer Paul Mullin',
        ),
    }
    return render(request, 'elections/bios/paul_mullin.html', context)
