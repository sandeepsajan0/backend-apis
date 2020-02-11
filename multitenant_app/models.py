from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from django_multitenant.fields import *
from django_multitenant.models import *
from .manager import UserManager, DocumentManager

# Create your models here.
class Company(TenantModel):
    tenant_id = "id"
    company_name = models.CharField(
        max_length=250, blank=False, null=False, unique=True
    )


class User(AbstractUser, TenantModel):
    company = models.ForeignKey(Company, on_delete=models.PROTECT)
    tenant_id = "company_id"
    email = models.EmailField(_("email"), unique=True)

    objects = UserManager()
    REQUIRED_FIELDS = ["email"]

    class Meta(object):
        unique_together = ["id", "company"]


class Document(TenantModel):
    doc_name = models.CharField(max_length=250, blank=False, null=False)
    doc_text = models.TextField(null=True, blank=True)
    company = models.ForeignKey(Company, on_delete=models.PROTECT)
    tenant_id = "company_id"
    user = TenantForeignKey(User, on_delete=models.CASCADE)

    objects = DocumentManager()
