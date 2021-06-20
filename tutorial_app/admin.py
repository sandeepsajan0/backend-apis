from django.contrib import admin

from .models import Idea, User

# Register your models here.
admin.site.register(Idea)
admin.site.register(User)
