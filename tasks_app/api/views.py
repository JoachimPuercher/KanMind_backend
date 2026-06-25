from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, mixins
from .serializers import TaskSerializerCommentsCount, CommentSerializer, TaskSerializer
from ..models import Board, Comment
from tasks_app.models import Task
from django.contrib.auth.models import User
from .permission import IsBoardMemberFromPayload, DenyAllUsers, IsBoardOwnerFromPayload, IsCommentOwner, IsBoardOwnerFromTask, IsTaskOwner, IsBoardMemberFromTask
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
# from .serializers import GetBoardSerializer, PostBoardSerializer
from django.db.models import Q
# from django.shortcuts import get_object_or_404





class TaskAssigneeList(generics.ListAPIView):
    serializer_class = TaskSerializerCommentsCount

    def get_queryset(self):
        return Task.objects.filter(Q(assignee=self.request.user)).distinct()



class TasksReviewingList(generics.ListAPIView):
    serializer_class = TaskSerializerCommentsCount
    
    def get_queryset(self):
        return Task.objects.filter(Q(reviewer=self.request.user)).distinct()
    

class PostTaskView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated, IsBoardOwnerFromPayload | IsBoardMemberFromPayload]
    serializer_class = TaskSerializerCommentsCount

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class UpdateDeleteTaskView(mixins.DestroyModelMixin, mixins.UpdateModelMixin, generics.GenericAPIView):
    serializer_class = TaskSerializer
    lookup_url_kwarg = "task_id"
    queryset = Task.objects.all()

    def get_permissions(self):
        if self.request.method == "DELETE":
            return [IsAuthenticated(), (IsTaskOwner | IsBoardOwnerFromTask)()]
        
        elif self.request.method == "PATCH":
            return [IsAuthenticated(), (IsBoardMemberFromTask | IsTaskOwner)()]

        else:
            return [DenyAllUsers()]
        
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

class TaskCommentView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, IsBoardMemberFromTask | IsBoardOwnerFromTask]
    serializer_class = CommentSerializer
    
    def get_queryset(self):
        return Comment.objects.filter(task_id=self.kwargs["task_id"]).all()

    def perform_create(self, serializer):
        task = get_object_or_404(Task, pk=self.kwargs["task_id"])
        serializer.save(author=self.request.user, task=task)

class DeleteCommentView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated, IsCommentOwner]
    lookup_url_kwarg = "comment_id"

    def get_queryset(self):
        return Comment.objects.filter(task_id=self.kwargs["task_id"]).all()