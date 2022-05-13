from datetime import datetime

from django.db.models import (
    Model,
    QuerySet,
    ManyToManyField,
    ForeignKey,
    OneToOneField,
    CharField,
    TextField,
    IntegerField,
    DateTimeField,
    PROTECT,
    CASCADE,
)
from abstracts.models import AbstractDateTime
from abstracts.validators import AbstractValidator


class Title(Model):
    """Title entity."""

    name = CharField(
        verbose_name='имя',
        max_length=50
    )
    link = TextField(
        verbose_name='ссылка'
    )

    class Meta:
        ordering = (
            '-id',
        )
        verbose_name = 'дата выпуска'
        verbose_name_plural = 'даты выпуска'

    def __str__(self) -> str:
        return f'Тайтл: {self.name}'


class ReleaseDate(Model):
    """ReleaseDate entity."""

    published = CharField(
        verbose_name='выпущен',
        max_length=20
    )
    date = DateTimeField(
        verbose_name='дата'
    )

    class Meta:
        ordering = (
            '-id',
        )
        verbose_name = 'дата выпуска '
        verbose_name_plural = 'даты выпуска '

    def __str__(self) -> str:
        return f'Дата выпуска: {self.published}'


class AnimeQuerySet(QuerySet):
    """Anime queryset."""

    def get_deleted(self) -> QuerySet['Anime']:
        return self.filter(
            datetime_deleted__isnull=False
        )

    def get_not_deleted(self) -> QuerySet['Anime']:
        return self.filter(
            datetime_deleted__isnull=True
        )


class Anime(AbstractDateTime, AbstractValidator):
    """Anime entity."""

    studio = CharField(
        verbose_name='студия',
        max_length=100,
        default=''
    )
    rating = IntegerField(
        verbose_name='рейтинг',
    )
    release_date = ForeignKey(
        ReleaseDate,
        on_delete=PROTECT,
        verbose_name='дата выпуска'
    )
    title = OneToOneField(
        Title,
        on_delete=CASCADE,
        verbose_name='название',
        null=True, blank=True
    )
    objects = AnimeQuerySet().as_manager()

    class Meta:
        ordering = (
            '-datetime_created',
        )
        verbose_name = 'аниме'
        verbose_name_plural = 'аниме'

    def __str__(self) -> str:
        return f'{self.studio} | {self.title.name}, {self.rating}'

    def clean(self) -> None:
        self.validate_release_date(
            self.release_date.date
        )

    def save(self, *args: tuple, **kwargs: dict) -> None:
        self.full_clean()
        super().save(*args, **kwargs)

    def delete(self) -> None:
        self.datetime_deleted = datetime.now()
        self.save(
            update_field=['datetime_deleted']
        )
        # super().delete()


class Description(Model):
    """Description entity."""

    anime = OneToOneField(
        Anime,
        on_delete=CASCADE,
        verbose_name='аниме',
        null=True, blank=True
    )
    text_en = TextField(
        verbose_name='текст на английском',
        default=''
    )
    text_ru = TextField(
        verbose_name='текст на русском',
        default=''
    )

    class Meta:
        ordering = (
            '-id',
        )
        verbose_name = 'описание'
        verbose_name_plural = 'описания'

    def __str__(self) -> str:
        return 'Описание тайтла'


class Genre(Model):
    """Genre entity."""

    name = CharField(
        verbose_name='имя',
        max_length=50
    )
    anime = ManyToManyField(
        Anime,
        related_name='genres',
        verbose_name='аниме'
    )

    class Meta:
        ordering = (
            'name',
        )
        verbose_name = 'жанр'
        verbose_name_plural = 'жанры'

    def __str__(self) -> str:
        return f'Жанр: {self.name}'
