from django.db import models
from django.contrib.auth.models import AbstractUser,User
from django.utils.translation import ugettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import datetime

# Create your models here.

class User(AbstractUser):
    username = None
    email = models.EmailField(_('email'), unique=True)
    name = models.CharField(max_length=250)
    avatar_url = models.URLField(blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

class Idea(models.Model):
    """
    Ideas model
    """
    content = models.CharField(max_length=256, blank=False, null=False)
    impact = models.IntegerField(validators=[MinValueValidator(1),
                                             MaxValueValidator(10)],
                                 blank=False, null=False)
    ease = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)],
                               blank=False, null=False)
    confidence = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)],
                                     blank=False, null=False)
    average_score = models.IntegerField(blank=True, null=False)
    created_at = models.DateTimeField(default=datetime.now, blank=True)