from django.contrib.auth.models import Group
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import permissions


def add_user_to_group(group_name, user):
    """
    Adding the user to a given group
    :return:
    """
    if group_name == "owner":
        user.is_superuser = True
        user.save()
    else:
        user.is_superuser = False
        user.save()
    try:
        group_obj = Group.objects.get(name=group_name)
    except ObjectDoesNotExist:
        raise
    if len(user.groups.all()) > 0:
        user.groups.clear()
    user.groups.add(group_obj)


class IsAuthorOwnerAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        group_admin = Group.objects.get(name="admin")
        group_owner = Group.objects.get(name="owner")
        if group_admin in request.user.groups.all():
            return True
        elif group_owner in request.user.groups.all():
            return True
        elif obj.author == request.user:
            return True
        else:
            return False
