from django.core.paginator import Paginator
from django.http import Http404
from django.shortcuts import render
from meta.views import Meta

from .models import News


def news_list(request):
    news = News.objects.published(request.user).order_by('-published')
    paginator = Paginator(news, 5)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    context = {
        'news': page,
        'meta': Meta(
            title='Recent News - Petersburg Democratic Committee',
            description='Recent news related to PDC and upcoming elections',
        ),
    }
    return render(request, 'news/list.html', context)


def news_item(request, year, month, day, slug):
    try:
        news = News.objects.published(request.user).get(
            slug=slug,
            published__year=year,
            published__month=month,
            published__day=day
        )
    except News.DoesNotExist:
        raise Http404()

    context = {
        'page': news,
        'meta': Meta(
            title=news.title,
            description=news.summary,
        ),
    }
    return render(request, 'news/detail.html', context)
