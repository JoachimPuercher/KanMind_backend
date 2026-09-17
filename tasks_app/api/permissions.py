"""Permissions of the tasks API."""
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import BasePermission
from boards_app.models import Board
from ..models import Comment, Task


def get_board_from_payload(request):
    """Return the payload board: 400 if the id is invalid, 404 if unknown."""
    try:
        board_id = int(request.data.get("board"))
    except (AttributeError, TypeError, ValueError):
        raise ValidationError({"board": "A valid board id is required."})

    return get_object_or_404(Board, pk=board_id)


class IsBoardMemberFromTaskPayload(BasePermission):
    """Allow members of the board referenced in the payload."""

    message = "You have no permission to access the board."

    def has_permission(self, request, view):
        """Return True if the user is a member of the payload board."""
        board = get_board_from_payload(request)

        return board.members.contains(request.user)


class IsBoardOwnerFromTaskPayload(BasePermission):
    """Allow the owner of the board referenced in the payload."""

    message = "You have no permission to access the board."

    def has_permission(self, request, view):
        """Return True if the user owns the payload board."""
        board = get_board_from_payload(request)

        return request.user == board.owner


class IsBoardMemberFromTask(BasePermission):
    """Allow members of the board the URL task belongs to."""

    def has_permission(self, request, view):
        """Return True if the user is a member of the task's board."""
        task = get_object_or_404(Task, pk=view.kwargs["task_id"])
        return bool(task.board.members.contains(request.user))


class IsBoardOwnerFromTask(BasePermission):
    """Allow the owner of the board the URL task belongs to."""

    def has_permission(self, request, view):
        """Return True if the user owns the task's board."""
        task = get_object_or_404(Task, pk=view.kwargs["task_id"])
        return task.board.owner == request.user


class IsTaskOwner(BasePermission):
    """Allow access only to the task's owner."""

    def has_object_permission(self, request, view, obj):
        """Return True if the user owns the task."""
        return request.user == obj.owner


class IsCommentOwner(BasePermission):
    """Allow a comment's author to delete it."""

    message = "No Permission to delete comment."

    def has_permission(self, request, view):
        """Allow only DELETE at the view level."""
        return request.method == "DELETE"

    def has_object_permission(self, request, view, obj: Comment):
        """Return True if the user authored the comment."""
        return request.user == obj.author


class DenyAllUsers(BasePermission):
    """Deny access to every user."""

    def has_permission(self, request, view):
        """Always deny the request."""
        return False
