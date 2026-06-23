from rest_framework.permissions import BasePermission
from ..models import Board
from ..models import Comment, Task
from django.shortcuts import get_object_or_404


class IsBoardMemberFromPayload(BasePermission):
    message = "You have no permission to access the board."

    def has_permission(self, request, view):
        board = Board.objects.filter(pk=request.data.get("board")).first()
        if board is None:
            self.message = "No board found to check permissions."
            return False
        
        return board.members.contains(request.user)
    

class IsBoardOwnerFromPayload(BasePermission):
    message = "You have no permission to access the board."

    def has_permission(self, request, view):
        board = Board.objects.filter(pk=request.data.get("board")).first()
        if board is None:
            self.message= "No board found to check permissions."
            return False
        
        return request.user == board.owner

class IsBoardMemberFromTask(BasePermission):

    def has_permission(self, request, view):
        task = get_object_or_404(Task, pk=view.kwargs["task_id"])
        return bool(task.board.members.contains(request.user))
        
class IsBoardOwnerFromTask(BasePermission):

    def has_permission(self, request, view):
        task = get_object_or_404(Task, pk=view.kwargs["task_id"])
        return task.board.owner == request.user
        

class IsBoardOwner(BasePermission):

    def has_permission(self, request, view):
        return request.method == "PATCH" or request.method == "DELETE"
    
    def has_object_permission(self, request, view, obj:Task):
        return request.user == obj.board.owner


class IsBoardMemberGetPost(BasePermission):

    def has_permission(self, request, view):
        method = bool(request.method == "GET" or request.method == "POST")
        task = get_object_or_404(Task, pk=view.kwargs["task_id"])
        is_member = task.board.members.contains(request.user)
        return bool(method and is_member)
    

class IsTaskOwner(BasePermission):

    def has_object_permission(self, request, view, obj):
        return request.user == obj.owner

class IsCommentOwner(BasePermission):
    message = "No Permission to delete comment."

    def has_permission(self, request, view):
        return request.method == "DELETE"
            
        
    def has_object_permission(self, request, view, obj:Comment):
        return request.user == obj.author
            