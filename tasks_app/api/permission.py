from rest_framework.permissions import BasePermission
from ..models import Board, Comment, Task
from django.shortcuts import get_object_or_404


class IsBoardMemberFromTaskPayload(BasePermission):
    """Allow members of the board referenced in the payload."""

    message = "You have no permission to access the board."

    def has_permission(self, request, view):
        """Return True if the user is a member of the payload board."""
        board = Board.objects.filter(pk=request.data.get("board")).first()
        if board is None:
            self.message = "No board found to check permissions."
            return False

        return board.members.contains(request.user)


class IsBoardOwnerFromTaskPayload(BasePermission):
    """Allow the owner of the board referenced in the payload."""

    message = "You have no permission to access the board."

    def has_permission(self, request, view):
        """Return True if the user owns the payload board."""
        board = Board.objects.filter(pk=request.data.get("board")).first()
        if board is None:
            self.message = "No board found to check permissions."
            return False

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


class IsBoardOwner(BasePermission):
    """Allow write methods only to the task's board owner."""

    def has_permission(self, request, view):
        """Allow only PATCH and DELETE at the view level."""
        return request.method == "PATCH" or request.method == "DELETE"

    def has_object_permission(self, request, view, obj: Task):
        """Return True if the user owns the task's board."""
        return request.user == obj.board.owner


class IsBoardMemberGetPost(BasePermission):
    """Allow GET and POST to members of the task's board."""

    def has_permission(self, request, view):
        """Return True for GET/POST when the user is a member."""
        method = bool(request.method == "GET" or request.method == "POST")
        task = get_object_or_404(Task, pk=view.kwargs["task_id"])
        is_member = task.board.members.contains(request.user)
        return bool(method and is_member)


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
