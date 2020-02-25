from django.contrib import admin
from .models import User, Idea

# Register your models here.
admin.site.register(Idea)
admin.site.register(User)
