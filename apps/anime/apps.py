from django.apps import AppConfig


class AnimeConfig(AppConfig):
    name = 'anime'

    def ready(self) -> None:
        import anime.signals  # noqa
