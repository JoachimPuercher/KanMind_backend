from rest_framework.permissions import BasePermission
from ..models import Board


class IsBoardOwner(BasePermission):
    """Allow access only to the board's owner."""

    def has_object_permission(self, request, view, obj: Board):
        """Return True if the user owns the board."""
        return obj.owner == request.user


class IsBoardMember(BasePermission):
    """Allow access only to members of the board."""

    def has_object_permission(self, request, view, obj: Board):
        """Return True if the user is a member of the board."""
        return bool(obj.members.contains(request.user))
