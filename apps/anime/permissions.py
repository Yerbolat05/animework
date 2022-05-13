from rest_framework.permissions import BasePermission
from rest_framework.request import Request as DRF_Request


class AnimePermission(BasePermission):
    """Determines permission for Anime."""

    def __init__(self) -> None:
        self._admin: bool = False
        self._user: bool = False

    def _initialize_permissions(
        self,
        request: DRF_Request
    ) -> None:
        """Initializing base permissions."""

        self._user = (
            request.user and
            request.user.is_active
        )
        self._admin = self._user and (
            request.user.is_staff and
            request.user.is_superuser
        )

    def has_permission(
        self,
        request: DRF_Request,
        view: 'AnimeViewSet'
    ) -> bool:
        """Has permissions."""

        self._initialize_permissions(
            request
        )
        if view.action in (
            'list',
            'retrieve',
            'create',
            'partial_update',
            'update',
        ):
            return self._user

        if view.action in (
            'destroy',
        ):
            return self._admin

        return False
