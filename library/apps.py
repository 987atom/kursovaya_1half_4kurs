from django.apps import AppConfig
from django.db.models.signals import post_migrate

class LibraryConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'library'

    def ready(self):
        from django.contrib.auth.models import Group

        def create_groups(sender, **kwargs):
            Group.objects.get_or_create(name='Администратор')
            Group.objects.get_or_create(name='Библиотекарь')
            Group.objects.get_or_create(name='Гость')

        post_migrate.connect(create_groups, sender=self)
