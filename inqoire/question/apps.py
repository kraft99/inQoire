from django.apps import AppConfig


class QuestionConfig(AppConfig):
    name = 'inqoire.question'

    def ready(self):
    	import inqoire.question.signals
