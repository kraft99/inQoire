from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = 'inqoire.users'

    def ready(self):
    	import inqoire.users.signals