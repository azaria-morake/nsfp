from django.apps import AppConfig


class NsfpCoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'nsfp_core'

    def ready(self):
        import nsfp_core.signals