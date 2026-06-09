from rest_framework.permissions import BasePermission
from ..models import Board

class IsBoardMember(BasePermission):
    message = "You have no permission to access the board."

    def has_permission(self, request, view):

        if request.method != "POST":
            return False

        board = Board.objects.filter(pk=request.data.get("board")).first()
        if board is None:
            self.message = "No board found to check permissions."
            return False
        
        return bool(request.user == board.owner or board.members.contains(request.user))
      
    