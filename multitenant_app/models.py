from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django_multitenant.fields import *
from django_multitenant.models import *

from _datetime import datetime


# Create your models here.
class Company(models.Model):
    company_name = models.CharField(
        max_length=250, blank=False, null=False, unique=True
    )
    url_prefix = models.CharField(max_length=100, unique=True, blank=False)


class CompanyTenant(models.Model):
    company = models.ForeignKey(Company, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class User(AbstractUser, CompanyTenant):
    email = models.EmailField(_("email"), unique=True)
    owner_of_company = models.ForeignKey(
        Company, on_delete=models.SET_NULL, related_name="owner", null=True, blank=True
    )
    REQUIRED_FIELDS = ["email"]


class Document(CompanyTenant):
    doc_name = models.CharField(max_length=250, blank=False, null=False)
    doc_text = models.TextField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
