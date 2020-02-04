from django.contrib.auth.models import Group
from django.core.exceptions import ObjectDoesNotExist
from .models import User


def add_user_to_group(group_name, user):
    """
    Adding the user to a given group
    :return:
    """
    if group_name == "owner":
        user.is_superuser = True
        user.save()
    try:
        group_obj = Group.objects.get(name=group_name)
    except ObjectDoesNotExist:
        raise
    if len(user.groups.all()) == 0:
        group_obj.user_set.add(user)
    else:
        user_group = User.groups.through.objects.get(user=user)
        user_group.group = group_obj
        user_group.save()
