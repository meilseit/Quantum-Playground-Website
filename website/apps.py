from django.apps import AppConfig
import sys

class WebsiteConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'website'

    def ready(self):
        if "runserver" not in sys.argv:
            return True
        from .models import FlagStart
        FlagStart.objects.all().delete()
        FlagStart.objects.create()
        print("initalizing....")
        print(FlagStart.objects.first().flag)
