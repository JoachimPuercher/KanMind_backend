from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from .serializers import TaskSerializer, CommentSerializer
from ..models import Board, Comment
from tasks_app.models import Task
from django.contrib.auth.models import User
from .permission import IsBoardMember, IsCommentOwner
from django.shortcuts import get_object_or_404

# from .serializers import GetBoardSerializer, PostBoardSerializer
from django.db.models import Q
# from django.shortcuts import get_object_or_404





class TaskListSelfAssignedView(APIView):

    def get(self, request):
        boards = Board.objects.filter(Q(owner=request.user) | Q(members=request.user)).distinct()
        print (boards)
    

class PostTaskView(generics.CreateAPIView):
    # permission_classes = [IsBoardMember]
    serializer_class = TaskSerializer



class UpdateDeleteTaskView(generics.DestroyAPIView, generics.UpdateAPIView):
    serializer_class = TaskSerializer
    permission_classes = []


class TaskCommentView(generics.ListCreateAPIView):
    permission_classes = []
    serializer_class = CommentSerializer
    
    def get_queryset(self):
        return Comment.objects.filter(task_id=self.kwargs["task_id"]).all()

    def perform_create(self, serializer):
        task = get_object_or_404(Task, pk=self.kwargs["task_id"])
        serializer.save(author=self.request.user, task=task)

class DeleteCommentView(generics.DestroyAPIView):
    permission_classes = [IsCommentOwner]
    lookup_url_kwarg = "comment_id"

    def get_queryset(self):
        return Comment.objects.filter(task_id=self.kwargs["task_id"]).all()
