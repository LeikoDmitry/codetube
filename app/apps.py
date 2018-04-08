from django.apps import AppConfig
import algoliasearch_django as algoliasearch


class AppConfig(AppConfig):
    name = 'app'

    def ready(self):
        channel = self.get_model('Channel')
        video = self.get_model('Video')
        algoliasearch.register(channel)
        algoliasearch.register(video)

