from django.contrib import admin
from solo.admin import SingletonModelAdmin
from .models import Announcement

# Admin setup
admin.site.site_header = 'PDC Admin Portal'
admin.site.index_title = 'PDC Site Administration'

admin.site.register(Announcement, SingletonModelAdmin)
