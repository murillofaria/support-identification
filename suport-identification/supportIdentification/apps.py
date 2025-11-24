from django.apps import AppConfig


class SupportidentificationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'supportIdentification'

    def ready(self):
        import supportIdentification.signals