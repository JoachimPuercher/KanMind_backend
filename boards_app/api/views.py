from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.contrib.auth.models import User
from ..models import Board
from .serializers import GetBoardSerializer
from django.db.models import Q

class AllBoardsView(APIView):
    """
    View to list all users in the system.

    * Requires token authentication.
    * Only admin users are able to access this view.
    """
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        """
        Return a list of all users.
        """
        boards = Board.objects.filter(
            Q(owner=request.user) | Q(members=request.user)
        ).distinct()
        serializer = GetBoardSerializer(boards, many=True)
        return Response(serializer.data)