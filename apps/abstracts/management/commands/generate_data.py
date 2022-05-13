from datetime import datetime

from django.core.management.base import BaseCommand

from auths.models import CustomUser


class Command(BaseCommand):
    """Custom command for filling up database."""

    help = 'Custom command for filling up database.'

    def __init__(self, *args: tuple, **kwargs: dict) -> None:
        super().__init__(args, kwargs)

    def _generate_users(self) -> None:
        """Generates CustomUser objects."""

        if not CustomUser.objects.filter(is_superuser=True).exists():
            superuser: dict = {
                'email': 'madi7maratovic@gmail.com',
                'password': '299792458',
            }
            CustomUser.objects.create_superuser(**superuser)

    def handle(self, *args: tuple, **kwargs: dict) -> None:
        """Handles data filling."""

        start: datetime = datetime.now()

        self._generate_users()

        print(
            'Generating Data: {} seconds'.format(
                (datetime.now()-start).total_seconds()
            )
        )
