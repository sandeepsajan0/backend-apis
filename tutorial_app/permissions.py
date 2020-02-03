from django.contrib.auth.models import Group
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# @receiver(post_save, sender=User)
def add_user_to_group(sender, instance, **kwargs):
    """

    :return:
    """
    if instance.user_group == "owner":
        instance.is_superuser = True
        instance.save()
    else:
        try:
            group = Group.objects.get(name=instance.user_group)
            group.user_set.add(instance)
        except ObjectDoesNotExist:
            raise
