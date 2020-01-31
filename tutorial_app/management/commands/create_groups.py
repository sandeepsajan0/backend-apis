from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand
from tutorial_app.models import User, Idea
import logging

GROUPS = ["owner", "admin", "staff"]
MODELS = ["user", "idea"]
ALLPERMISSIONS = ["view", "add", "delete", "change"]


class Command(BaseCommand):
    help = "Creates default permissions groups for users"

    def handle(self, *args, **options):
        """

        :param args:
        :param options:
        :return:
        """
        for group in GROUPS:
            new_group, created = Group.objects.get_or_create(name=group)
            if group == "staff":
                model = "idea"
                for permission in ALLPERMISSIONS:
                    self.set_permission(permission, model, new_group)
                self.set_permission("view", "user", new_group)
            else:
                for model in MODELS:
                    for permission in ALLPERMISSIONS:
                        self.set_permission(permission, model, new_group)

            print("Created default group and permissions.")

    def set_permission(self, permission, model, group):
        """

        :param permission:
        :param model:
        :param group:
        :return:
        """
        name = "Can {} {}".format(permission, model)
        print("Creating {}".format(name))

        try:
            model_add_perm = Permission.objects.get(name=name)
            group.permissions.add(model_add_perm)
        except Permission.DoesNotExist:
            logging.warning("Permission not found with name '{}'.".format(name))
