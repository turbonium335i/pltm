from django.apps import AppConfig


class CbtsystemConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cbtsystem'


    def ready(self):
        import cbtsystem.signals

