from typing import Optional
from datetime import datetime

from requests import get as r_get
from requests.models import Response

from django.core.management.base import BaseCommand

from anime.models import (
    Description,
    Title,
    ReleaseDate,
    Anime,
    Genre,
)


class Command(BaseCommand):
    """Custom command for filling up database from JSON."""

    help = 'Custom command for filling up database from JSON.'

    def __init__(self, *args: tuple, **kwargs: dict) -> None:
        pass

    def __get_generated_release_date(
        self,
        start_date: str
    ) -> Optional[ReleaseDate]:
        """Generates ReleaseDate object."""

        month_map: dict = {
            'Jan': '01',
            'Feb': '02',
            'Mar': '03',
            'Apr': '04',
            'May': '05',
            'Jun': '06',
            'Jul': '07',
            'Aug': '08',
            'Sep': '09',
            'Oct': '10',
            'Nov': '11',
            'Dec': '12',
        }
        published: str = start_date.split(' (')[0]

        month: str = published[0:3]        # 'Apr'
        month_num: str = month_map[month]  # '04'

        custom_published: str = published.replace(
            month,
            month_num
        )
        month_day: str
        year: str
        time: str
        try:
            month_day, year, time = custom_published.split(',')
        except ValueError:
            month_day, year = custom_published.split(',')
            time = '00:00'

        year = year.replace(' ', '')
        time = time.replace(' ', '')

        _: str
        day: str
        _, day = month_day.split(' ')

        day_str: str = day
        if len(day) == 1:
            day_str: str = ''.join(
                [
                    '0',
                    day
                ]
            )
        date_time_str: str = f'{day_str}/{month_num}/{year} {time}'

        date: datetime = datetime.strptime(
            date_time_str,
            '%d/%m/%Y %H:%M'
        )
        release_date: Optional[ReleaseDate] = \
            ReleaseDate.objects.get_or_create(
                published=published,
                date=date
            )
        return release_date

    def _generate_anime(self) -> None:
        """Generates Anime objects."""

        anime_public_resource_url: str = \
            'https://raw.githubusercontent.com/asarode/anime-list/master/data/data.json'  # noqa

        # Делаем запрос в открытый источник методом GET
        #
        response: Response = r_get(anime_public_resource_url)

        if response.status_code != 200:
            return None

        data: list = response.json()
        obj: dict
        for obj in data:
            title: Title
            created: bool
            title, created = \
                Title.objects.get_or_create(
                    name=obj['title']['text'],
                    link=obj['title']['link']
                )
            description: Description
            created: bool
            description, created = \
                Description.objects.get_or_create(
                    text_en=obj['description']
                )
            release_date: ReleaseDate
            created: bool
            release_date, created = \
                self.__get_generated_release_date(
                    obj['start_date']
                )
            anime: Anime
            created: bool
            anime, created = \
                Anime.objects.get_or_create(
                    studio=obj.get(
                        'studio',
                        'Unknown'
                    ),
                    rating=obj['hype'],
                    title=title,
                    description=description,
                    release_date=release_date
                )
            # Генерируем жанры (Genre)
            #
            genre: str
            for genre in obj['genres']:
                name: str = genre if genre != '-' else 'Unknown'
                genre: Genre
                created: bool
                genre, created = \
                    Genre.objects.get_or_create(
                        name=name
                    )
                anime.genres.add(genre)

    def handle(self, *args: tuple, **kwargs: dict) -> None:
        """Handles data filling."""

        start: datetime = datetime.now()

        self._generate_anime()

        print(
            'Generating Data: {} seconds'.format(
                (datetime.now()-start).total_seconds()
            )
        )
