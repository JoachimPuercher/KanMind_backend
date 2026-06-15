from rest_framework.permissions import BasePermission
from ..models import Board
from ..models import Comment

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
      
class IsCommentOwner(BasePermission):
    message = "No Permission to delete comment."

    def has_permission(self, request, view):
        return request.method == "DELETE"
            
        
    def has_object_permission(self, request, view, obj:Comment):
        return request.user == obj.author
            