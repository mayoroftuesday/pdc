from django.shortcuts import render
from meta.views import Meta

from .models import Page


def generic_page(request, slug):
    page = Page.objects.published(request.user).get(slug=slug)
    context = {
        'page': page,
        'meta': Meta(
            title=page.title,
            description=page.summary,
        ),
    }
    return render(request, 'pages/page.html', context)
