from django.apps import AppConfig


class CommonAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'COMMON_APP'
   
    def ready(self):
        import COMMON_APP.signals 


