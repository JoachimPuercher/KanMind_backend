from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions, status, generics
from .serializers import TaskSerializer
from ..models import Board
# from .serializers import GetBoardSerializer, PostBoardSerializer
from django.db.models import Q
# from django.shortcuts import get_object_or_404





class TaskListSelfAssignedView(APIView):

    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        boards = Board.objects.filter(Q(owner=request.user) | Q(members=request.user)).distinct()
        print (boards)
    

class PostTaskView(generics.CreateAPIView):
    serializer_class = TaskSerializer