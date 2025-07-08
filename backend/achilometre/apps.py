from django.apps import AppConfig


class AchilometreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'achilometre'

    def ready(self):
        import achilometre.signal
