from rest_framework.permissions import BasePermission
from ..models import Board

class IsBoardOwner(BasePermission):
    def has_object_permission(self, request, view, obj:Board):
        return obj.owner == request.user
    
class IsBoardMember(BasePermission):
    def has_object_permission(self, request, view, obj:Board):
        return bool(obj.members.contains(request.user))
