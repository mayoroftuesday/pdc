from django.core.mail import mail_admins
from django.shortcuts import render
from meta.views import Meta

from .models import Announcement
from .forms import ContactForm
from news.models import News
from events.models import EventOccurrence


def home(request):
    try:
        announcement = Announcement.objects.get()
    except Announcement.DoesNotExist:
        announcement = None

    top_news = News.objects.published(request.user).all()[:3]

    events = EventOccurrence.objects.published(request.user)
    upcoming_events = events.upcoming().all()[:3]

    context = {
        'announcement': announcement,
        'top_news': top_news,
        'events': upcoming_events,
        'show_breadcrumbs': False,
        'meta': Meta(
            title='Home - Petersburg Democratic Committee',
            description='Homepage for the Petersburg Democratic Committee',
        ),
    }

    return render(request, 'pdc/home.html', context)


def act(request):
    context = {
        'meta': Meta(
            title='Action - Petersburg Democratic Committee',
            description=(
                'Take action today to help promote Democrats in the '
                'Petersburg area by volunteering, donating, or joining the '
                'committee'
            ),
        ),
    }
    return render(request, 'pdc/act.html', context)


def info(request):
    context = {
        'meta': Meta(
            title='Information - Petersburg Democratic Committee',
            description=(
                'Learn about PDC, recent news, upcoming events, and upcoming '
                'elections'
            ),
        ),
    }
    return render(request, 'pdc/info.html', context)


def about(request):
    context = {
        'meta': Meta(
            title='About PDC - Petersburg Democratic Committee',
            description='Learn about Petersburg Democratic Committee',
        ),
    }
    return render(request, 'pdc/about.html', context)


def join(request):
    context = {
        'meta': Meta(
            title='Join - Petersburg Democratic Committee',
            description='Learn how to join PDC and pay dues',
        ),
    }
    return render(request, 'pdc/join.html', context)


def donate(request):
    context = {
        'meta': Meta(
            title='Donate - Petersburg Democratic Committee',
            description='Make a donation to PDC',
        ),
    }
    return render(request, 'pdc/donate.html', context)


def volunteer(request):
    context = {
        'meta': Meta(
            title='Volunteer - Petersburg Democratic Committee',
            description='Volunteer your time with Petersburg Democrats',
        ),
    }
    return render(request, 'pdc/volunteer.html', context)


def contact(request):

    show_thank_you = False

    if request.method == 'POST':
        form = ContactForm(request.POST)
        data = form.data

        if form.is_valid():
            subject = (
                "Contact Form Submitted: "
                f"{data['your_name']} <{data['email']}>"
            )
            # ensure subject does not contain newlines
            subject = subject.replace("\n", "").replace("\r", "")
            message = "\n".join([
                "Contact form submitted:",
                f"Name: {data['your_name']}",
                f"Email: {data['email']}",
                f"Phone: {data['phone']}",
                f"Subject: {data['subject']}",
                f"Message:\n{data['message']}",
            ])

            mail_admins(subject, message)
            show_thank_you = True
    else:
        form = ContactForm()

    context = {
        'meta': Meta(
            title='Contact - Petersburg Democratic Committee',
            description=(
                'Get in touch with the Petersburg Democratic Committee if you '
                'need more information or need assistance with voting'
            )
        ),
        'form': form,
        'show_thank_you': show_thank_you,
    }

    return render(request, 'pdc/contact.html', context)
