from django_multitenant.mixins import *
from django.db import models


class UserManager(TenantManagerMixin, models.Manager):
    pass


class DocumentManager(TenantManagerMixin, models.Manager):
    pass
