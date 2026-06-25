from rest_framework import serializers
from ..models import Task
from tasks_app.models import Comment
from django.contrib.auth.models import User


class MemberSerializer(serializers.ModelSerializer):
    fullname = serializers.CharField(source="userprofile.fullname", read_only=True)
    
    class Meta:
        model = User
        fields = ["id", "fullname", "email"]
        read_only_fields = ["email", "id", "fullname"]


class TaskSerializerCommentsCount(serializers.ModelSerializer):

    assignee = MemberSerializer(read_only=True)
    reviewer = MemberSerializer(read_only=True)
    assignee_id = serializers.PrimaryKeyRelatedField(
         queryset=User.objects.all(), write_only=True, source="assignee", required=False
    )
    reviewer_id = serializers.PrimaryKeyRelatedField(
         queryset=User.objects.all(), write_only=True, source="reviewer", required=False
    )
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = ["board", "title", "description", "status", "priority", "assignee", "assignee_id", "reviewer", "reviewer_id", "due_date", "comments_count"]

    def get_comments_count(self, obj):
        return obj.comments.count()
    
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
        fields = ["title", "description", "status", "priority", "assignee", "assignee_id", "reviewer", "reviewer_id", "due_date"]
        read_only_fields = ["id"]


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()

    # The obj is the Meta class model
    def get_author(self, obj:Comment):
        return obj.author.userprofile.fullname
    class Meta:
        model = Comment
        fields = ["id", "created_at", "author", "content"]
        read_only_fields = ["id", "created_at", "author"]

    