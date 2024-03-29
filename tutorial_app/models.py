from datetime import datetime

from django.contrib.auth.models import AbstractUser, User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import ugettext_lazy as _

from .manager import UserManager

# Create your models here.


class User(AbstractUser):
    username = None
    USER_TYPES = (("owner", "owner"), ("admin", "admin"), ("staff", "staff"))
    email = models.EmailField(_("email"), unique=True)
    name = models.CharField(max_length=250)
    avatar_url = models.URLField(blank=True, null=True)
    user_group = models.CharField(max_length=50, choices=USER_TYPES, default="staff")
    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]


class Idea(models.Model):
    """
    Ideas model
    """

    content = models.CharField(max_length=256, blank=False, null=False)
    impact = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        blank=False,
        null=False,
    )
    ease = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        blank=False,
        null=False,
    )
    confidence = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        blank=False,
        null=False,
    )
    average_score = models.IntegerField(blank=True, null=False)
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
