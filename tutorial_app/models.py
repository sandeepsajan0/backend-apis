from django.db import models
from django.contrib.auth.models import AbstractUser,User
from django.utils.translation import ugettext_lazy as _

# Create your models here.

class User(AbstractUser):
    username = None
    email = models.EmailField(_('email'), unique=True)
    name = models.CharField(max_length=250)
    avatar_url = models.URLField(blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']