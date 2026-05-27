from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions, status
from ..models import Board
from .serializers import GetBoardSerializer, PostBoardSerializer
from django.db.models import Q

class BoardListView(APIView):

    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        boards = Board.objects.filter(
            Q(owner=request.user) | Q(members=request.user)
        ).distinct()
        serializer = GetBoardSerializer(boards, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PostBoardSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        board = serializer.save(owner=request.user)
        response = GetBoardSerializer(board)
        return Response (response.data, status=status.HTTP_201_CREATED)
