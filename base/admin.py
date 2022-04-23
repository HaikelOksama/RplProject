from django.contrib import admin
from .models import Fakultas, Organisasi, Topic, Event, Feed, UserProfile


# Register your models here.

admin.site.register(Organisasi)
admin.site.register(Topic)
admin.site.register(Event)
admin.site.register(Feed)
admin.site.register(UserProfile)
admin.site.register(Fakultas)