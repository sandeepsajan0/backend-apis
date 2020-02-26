from django.contrib.auth.models import BaseUserManager
from .permissions import add_user_to_group


class UserManager(BaseUserManager):
    def create_superuser(self, email, password, **kwargs):
        user = self.model(
            email=email, user_group="owner", is_staff=True, is_superuser=True, **kwargs
        )
        user.set_password(password)
        add_user_to_group("owner", user)
        user.save()
        return user
