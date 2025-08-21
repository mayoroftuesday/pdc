from django.contrib import admin
from .models import News


class NewsAdmin(admin.ModelAdmin):
    model = News
    list_display = ('title', 'published')


admin.site.register(News, NewsAdmin)
