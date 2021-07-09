from django.apps import AppConfig


class TutoConfig(AppConfig):
    name = 'tuto'
    
    def ready(self):
        import tuto.signals