from django.db.models.signals import (
    pre_save,
    post_save,
    pre_delete,
    post_delete,
)
from django.dispatch import receiver
from django.db.models.base import ModelBase

from abstracts.utils import send_email
from anime.models import Anime


@receiver(
    post_save,
    sender=Anime
)
def post_save_anime(
    sender: ModelBase,
    instance: Anime,
    created: bool,
    **kwargs: dict
) -> None:
    """Signal post-save Anime."""

    # Sending Email to User linked to Anime as uploader
    #
    send_email(
        'DJANGO_SUBJECT',
        'DJANGO_TEXT',
        'madi7maratovic@gmail.com'
    )


@receiver(
    pre_save,
    sender=Anime
)
def pre_save_anime(
    sender: ModelBase,
    instance: Anime,
    **kwargs: dict
) -> None:
    """Signal pre-save Anime."""
    pass

    # instance.save()


@receiver(
    post_delete,
    sender=Anime
)
def post_delete_anime(
    sender: ModelBase,
    instance: Anime,
    **kwargs: dict
) -> None:
    """Signal post-delete Anime."""

    instance.delete()


@receiver(
    pre_delete,
    sender=Anime
)
def pre_delete_anime(
    sender: ModelBase,
    instance: Anime,
    **kwargs: dict
) -> None:
    """Signal pre-delete Anime."""

    instance.delete()
