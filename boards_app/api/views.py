from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import Board
from .serializers import GetBoardSerializer, PostBoardSerializer
from django.db.models import Q
from django.shortcuts import get_object_or_404

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

    def get(self, request, pk):
        board = get_object_or_404(
            Board.objects.filter(Q(owner=request.user) | Q(members=request.user)).distinct(),
            pk=pk)
        serializer = GetBoardSerializer(board)
        return Response (serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, pk):
            board = get_object_or_404(
                Board.objects.filter(Q(owner=request.user) | Q(members=request.user)).distinct(),
                pk=pk)
            serializer = PostBoardSerializer(board, request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            updatedBoard = GetBoardSerializer(board)
            return Response (updatedBoard.data, status=status.HTTP_200_OK)
    
    def delete(self, request, pk):
            board = get_object_or_404(
                Board.objects.filter(Q(owner=request.user)).distinct(),
                pk=pk)
            board.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)