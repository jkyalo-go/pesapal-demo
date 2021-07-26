import os
from django.apps import AppConfig


class WebappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'webapp'

    def ready(self):
        from webapp.views import schedule_send_mail
        if os.environ.get('RUN_MAIN', None) != 'true':
            schedule_send_mail()
