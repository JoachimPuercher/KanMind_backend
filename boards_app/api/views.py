from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import Board
from .serializers import GetBoardSerializer, PatchBoardDetailSerializer, UpdateBoardDetailSerializer, GetBoardDetailSerializer, PostBoardSerializer
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from .permissions import IsBoardOwner, IsBoardMember


class BoardListView(APIView):

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

class BoardDetailView(APIView):

    def get_permissions(self):
         if self.request.method == "GET" or self.request.method == "PATCH":
              return [IsAuthenticated(), (IsBoardOwner | IsBoardMember)()]

         elif self.request.method == "DELETE":
              return [IsAuthenticated(), IsBoardOwner()]
         
         return False

    def get(self, request, board_id):
        board = get_object_or_404(
            Board.objects.filter(pk=board_id))
        self.check_object_permissions(request, board)
        serializer = GetBoardDetailSerializer(board)
        return Response (serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, board_id):
            board = get_object_or_404(
                Board.objects.filter(pk=board_id))
            self.check_object_permissions(request, board)
            serializer = PatchBoardDetailSerializer(board, request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            updatedBoard = UpdateBoardDetailSerializer(board)
            return Response (updatedBoard.data, status=status.HTTP_200_OK)
    
    def delete(self, request, board_id):
            board = get_object_or_404(
                Board.objects.filter(pk=board_id))
            self.check_object_permissions(request, board)
            board.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)