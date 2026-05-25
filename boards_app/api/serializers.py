from rest_framework import serializers
from boards_app.models import Board
from tasks_app.models import Status, Priority

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
    
