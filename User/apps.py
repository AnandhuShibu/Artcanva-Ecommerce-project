from django.apps import AppConfig


class UserConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'User'

# apps.py
from django.apps import AppConfig

class UserConfig(AppConfig):
    name = 'User'

    def ready(self):
        import User.signals  # Import your signals to make sure they are connected
