from rest_framework import generics, mixins
from .serializers import (TaskSerializerCommentsCount,
                          CommentSerializer, TaskSerializer)
from ..models import Comment
from tasks_app.models import Task
from .permission import (IsBoardMemberFromTaskPayload,
                         DenyAllUsers, IsBoardOwnerFromTaskPayload,
                         IsCommentOwner, IsBoardOwnerFromTask,
                         IsTaskOwner, IsBoardMemberFromTask)
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q


class TaskAssigneeList(generics.ListAPIView):
    """List tasks assigned to the current user."""

    serializer_class = TaskSerializerCommentsCount

    def get_queryset(self):
        """Return tasks where the user is the assignee."""
        return Task.objects.filter(Q(assignee=self.request.user)).distinct()


class TasksReviewingList(generics.ListAPIView):
    """List tasks the current user is reviewing."""

    serializer_class = TaskSerializerCommentsCount

    def get_queryset(self):
        """Return tasks where the user is the reviewer."""
        return Task.objects.filter(Q(reviewer=self.request.user)).distinct()


class PostTaskView(generics.CreateAPIView):
    """Create a task on a board the user owns or belongs to."""

    permission_classes = [IsAuthenticated,
                          IsBoardOwnerFromTaskPayload |
                          IsBoardMemberFromTaskPayload]
    serializer_class = TaskSerializerCommentsCount

    def perform_create(self, serializer):
        """Save the task with the requesting user as owner."""
        serializer.save(owner=self.request.user)


class UpdateDeleteTaskView(mixins.DestroyModelMixin,
                           mixins.UpdateModelMixin,
                           generics.GenericAPIView):
    """Update or delete a single task."""

    serializer_class = TaskSerializer
    lookup_url_kwarg = "task_id"
    queryset = Task.objects.all()

    def get_permissions(self):
        """Return permissions based on the request method."""
        if self.request.method == "DELETE":
            return [IsAuthenticated(), (IsTaskOwner | IsBoardOwnerFromTask)()]

        elif self.request.method == "PATCH":
            return [IsAuthenticated(), (IsBoardMemberFromTask | IsTaskOwner)()]

        else:
            return [DenyAllUsers()]

    def patch(self, request, *args, **kwargs):
        """Partially update the task."""
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        """Delete the task."""
        return self.destroy(request, *args, **kwargs)


class TaskCommentView(generics.ListCreateAPIView):
    """List and create comments on a task."""

    permission_classes = [IsAuthenticated,
                          IsBoardMemberFromTask | IsBoardOwnerFromTask]
    serializer_class = CommentSerializer

    def get_queryset(self):
        """Return all comments for the given task."""
        return Comment.objects.filter(task_id=self.kwargs["task_id"]).all()

    def perform_create(self, serializer):
        """Save the comment with its author and task."""
        task = get_object_or_404(Task, pk=self.kwargs["task_id"])
        serializer.save(author=self.request.user, task=task)


class DeleteCommentView(generics.DestroyAPIView):
    """Delete a comment (author only)."""

    permission_classes = [IsAuthenticated, IsCommentOwner]
    lookup_url_kwarg = "comment_id"

    def get_queryset(self):
        """Return the comments for the given task."""
        return Comment.objects.filter(task_id=self.kwargs["task_id"]).all()
