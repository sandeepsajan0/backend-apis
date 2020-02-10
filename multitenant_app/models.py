from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _

# Create your models here.
class Company(models.Model):
    name = models.CharField(max_length=250, blank=False, null=False, unique=True)
    password = models.CharField(max_length=50, null=False, blank=False)


class User(AbstractUser):
    email = models.EmailField(_("email"), unique=True)
    name = models.CharField(max_length=250)

    REQUIRED_FIELDS = ["name"]
