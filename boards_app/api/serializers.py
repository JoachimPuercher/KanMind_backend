from rest_framework import serializers
from boards_app.models import Board
from tasks_app.models import Status, Priority
from user_auth_app.models import User
from tasks_app.api.serializers import MemberSerializer, TaskSerializerCommentsCount

class GetBoardSerializer(serializers.ModelSerializer):

    member_count = serializers.SerializerMethodField()
    ticket_count = serializers.SerializerMethodField()
    tasks_to_do_count = serializers.SerializerMethodField()
    tasks_high_prio_count = serializers.SerializerMethodField()

    class Meta:
        model = Board
        fields = ["id", "title", "member_count", "ticket_count", "tasks_to_do_count", "tasks_high_prio_count", "owner_id"]

    def get_member_count(self, board):
        return board.members.count()

    def get_ticket_count(self, board):
        return board.tasks.count()
    
    def get_tasks_to_do_count(self, board):
        return board.tasks.filter(status=Status.TO_DO).count()
    
    def get_tasks_high_prio_count(self, board):
        return board.tasks.filter(priority=Priority.HIGH).count()
    

class PostBoardSerializer(serializers.ModelSerializer):
    members = serializers.PrimaryKeyRelatedField(many=True, queryset=User.objects.all())
    class Meta:
        model = Board
        fields = ["title", "members"]


class GetBoardDetailSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    title = serializers.CharField(max_length=200, read_only=True)
    owner_id = serializers.IntegerField(read_only=True)
    members = MemberSerializer(read_only=True, many=True)
    tasks = TaskSerializerCommentsCount(read_only=True, many=True)


class UpdateBoardDetailSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    title = serializers.CharField(read_only=True, max_length=200)
    owner_data = MemberSerializer(source="owner", many=False)
    members_data = MemberSerializer(source="members", many=True)


class PatchBoardDetailSerializer(serializers.ModelSerializer):
       class Meta:
        model = Board
        fields = ["title", "members"]