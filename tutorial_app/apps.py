from django.apps import AppConfig
from django.db.models.signals import post_save


class TutorialAppConfig(AppConfig):
    name = "tutorial_app"

    def ready(self):
        import tutorial_app.signals
