from django.contrib import admin
from .models import User, Idea

# Register your models here.
admin.site.register(Idea)
admin.site.register(User)


# class ModelAdmin(admin.ModelAdmin):
#     def save_model(self, request, obj, form, change):
#         obj.save(form=form)
