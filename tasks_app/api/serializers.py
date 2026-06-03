from rest_framework import serializers
from ..models import Task
from django.contrib.auth.models import User


class MemberSerializer(serializers.ModelSerializer):
    fullname = serializers.CharField(source="userprofile.fullname", read_only=True)
    
    class Meta:
        model = User
        fields = ["id", "fullname", "email"]
        read_only_fields = ["email", "id", "fullname"]


class TaskSerializer(serializers.ModelSerializer):

    assignee = MemberSerializer(read_only=True)
    reviewer = MemberSerializer(read_only=True)
    assignee_id = serializers.PrimaryKeyRelatedField(
         queryset=User.objects.all(), write_only=True, source="assignee", required=False
    )
    reviewer_id = serializers.PrimaryKeyRelatedField(
         queryset=User.objects.all(), write_only=True, source="reviewer", required=False
    )

    class Meta:
        model = Task
        fields = ["board", "title", "description", "status", "priority", "assignee", "assignee_id", "reviewer", "reviewer_id", "due_date"]

